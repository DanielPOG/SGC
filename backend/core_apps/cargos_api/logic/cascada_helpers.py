# ------------------------------------------------------------
# File: core_apps/cargos_api/logic/cascada_helpers.py
# ------------------------------------------------------------
from typing import Optional, Set
from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import ValidationError as DRFValidationError


from core_apps.cargos_api.models import CargoUsuario, EstadoVinculacion
from core_apps.usuarios_api.models import Usuario




def devolver_a_planta(usuario: Usuario, hoy=None, visited: Optional[Set[int]] = None, modo: str = "auto", context: Optional[dict] = None):
    """
    Intento de devolver `usuario` a su último cargo PLANTA conocido.


    Comportamiento:
    - Si el cargo está libre -> crea un CargoUsuario PLANTA para `usuario`.
    - Si está ocupado -> marca fechaRetiro al ocupante, crea la PLANTA para `usuario`
    y llama recursivamente para intentar devolver al ocupante retirado a su planta.


    Parámetros:
    - usuario: instancia de Usuario a devolver a planta
    - hoy: datetime/date a usar como fecha (por defecto timezone.now())
    - visited: conjunto de user.pk para evitar loops
    - modo: str opcional (no usado internamente, útil para trazabilidad)
    - context: dict opcional que se pasará como context al serializer (ej: {'cargo_destino_id': ...})


    Devuelve: la instancia de CargoUsuario creada para quien se devuelve (o None si no aplica)
    """
    if hoy is None:
        hoy = timezone.now()


    if visited is None:
        visited = set()


    # prevención de loops
    if usuario.pk in visited:
        return None
    visited.add(usuario.pk)


    # buscar último PLANTA conocido del usuario
    planta_hist = CargoUsuario.objects.filter(
    usuario=usuario,
    estadoVinculacion__estado__iexact="PLANTA"
    ).order_by("-fechaInicio").first()


    if not planta_hist:
        # Sin histórico PLANTA -> nada que devolver
        return None


    cargo_obj = planta_hist.cargo


    # Buscar ocupante activo (si existe) distinto al propio usuario
    ocupante = CargoUsuario.objects.filter(
    cargo=cargo_obj,
    fechaRetiro__isnull=True
    ).exclude(usuario=usuario).select_related("usuario").first()


    try:
        id_planta = EstadoVinculacion.objects.get(estado__iexact="PLANTA").id
    except EstadoVinculacion.DoesNotExist:
        raise DRFValidationError("No existe EstadoVinculacion 'PLANTA'")


    with transaction.atomic():
        # Si el cargo está libre -> crear registro PLANTA para usuario
        if ocupante is None:
            datos = {
            "num_doc": usuario.num_doc,
            "cargo": cargo_obj.id,
            "estadoVinculacion": id_planta,
            "salario": planta_hist.salario or 0,
            "grado": planta_hist.grado or "",
            "resolucion": planta_hist.resolucion or "",
            "resolucion_archivo": None,
            }
            # Importar el serializer dentro de la función para evitar imports circulares
            from core_apps.cargos_api.serializers import CargoUsuarioSerializer


            ser = CargoUsuarioSerializer(data=datos, context=context or {})
            ser.is_valid(raise_exception=True)
            nuevo = ser.save()


            usuario.cargo = cargo_obj
            usuario.save(update_fields=["cargo"])


            return nuevo
        
        # Si hay ocupante -> retirarlo y crear registro PLANTA para `usuario`
        else:
            ocupante.fechaRetiro = hoy
            ocupante.save(update_fields=["fechaRetiro"])


            datos = {
            "num_doc": usuario.num_doc,
            "cargo": cargo_obj.id,
            "estadoVinculacion": id_planta,
            "salario": planta_hist.salario or 0,
            "grado": planta_hist.grado or "",
            "resolucion": planta_hist.resolucion or "",
            "resolucion_archivo": None,
            "observacion": "Devolución escalonada a planta (ocupante retirado)",
            "fechaInicio": hoy,
            "fechaRetiro": None,
            }


            from core_apps.cargos_api.serializers import CargoUsuarioSerializer
            ser = CargoUsuarioSerializer(data=datos, context=context or {})
            ser.is_valid(raise_exception=True)
            nuevo_planta = ser.save()


            usuario.cargo = cargo_obj
            usuario.save(update_fields=["cargo"])


            # Recursión para el usuario que fue retirado
            devolver_a_planta(ocupante.usuario, hoy=hoy, visited=visited, modo=modo, context=context)


            return nuevo_planta