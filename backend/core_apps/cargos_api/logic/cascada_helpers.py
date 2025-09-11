# ------------------------------------------------------------
# File: core_apps/cargos_api/logic/cascada_helpers.py
# ------------------------------------------------------------
from typing import Optional, Set
from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import ValidationError as DRFValidationError


from core_apps.cargos_api.models import CargoUsuario, EstadoVinculacion
from core_apps.usuarios_api.models import Usuario
from core_apps.cargos_api.serializers import CargoUsuarioSerializer




def devolver_a_planta(
    usuario: Usuario,
    visited: Optional[Set[int]] = None,
    context: Optional[dict] = None
):
    """
    Devuelve a un usuario a su último cargo PLANTA conocido.
    - Si el cargo está libre -> crea CargoUsuario PLANTA.
    - Si está ocupado -> cierra al ocupante y crea PLANTA para usuario,
      luego recursivamente devuelve al ocupante a su PLANTA.
    """

    if visited is None:
        visited = set()

    if usuario.pk in visited:
        return None
    visited.add(usuario.pk)

    # Último PLANTA conocido
    planta_hist = CargoUsuario.objects.filter(
        usuario=usuario,
        estadoVinculacion__estado__iexact="PLANTA"
    ).order_by("-fechaInicio").first()

    if not planta_hist:
        return None

    cargo_obj = planta_hist.cargo

    try:
        estado_planta = EstadoVinculacion.objects.get(estado__iexact="PLANTA")
    except EstadoVinculacion.DoesNotExist:
        raise DRFValidationError("No existe EstadoVinculacion 'PLANTA'")

    # 🚨 Evitar duplicados: si ya tiene PLANTA activo en ese cargo, no hacer nada
    ya_tiene_planta = CargoUsuario.objects.filter(
        usuario=usuario,
        cargo=cargo_obj,
        estadoVinculacion=estado_planta,
        fechaRetiro__isnull=True
    ).exists()
    if ya_tiene_planta:
        return None

    # Buscar ocupante activo distinto al propio usuario
    ocupante = CargoUsuario.objects.filter(
        cargo=cargo_obj,
        fechaRetiro__isnull=True
    ).exclude(usuario=usuario).select_related("usuario").first()

    hoy = timezone.now()

    with transaction.atomic():
        # Cargo libre -> crear PLANTA para usuario
        if ocupante is None:
            datos = {
                "num_doc": usuario.num_doc,
                "cargo_id": cargo_obj.id,
                "estadoVinculacion": estado_planta.id,
                "salario": planta_hist.salario or 0,
                "grado": planta_hist.grado or "",
                "resolucion": planta_hist.resolucion or "",
                "resolucion_archivo": None,
                "observacion": "Devolución a PLANTA (libre)",
                "fechaInicio": hoy,
            }
            ser = CargoUsuarioSerializer(data=datos, context=context or {})
            ser.is_valid(raise_exception=True)
            nuevo = ser.save()

            usuario.cargo = cargo_obj
            usuario.save(update_fields=["cargo"])
            return nuevo

        # Cargo ocupado -> cerrar ocupante y crear PLANTA para usuario
        else:
            ocupante.fechaRetiro = hoy
            ocupante.save(update_fields=["fechaRetiro"])

            datos = {
                "num_doc": usuario.num_doc,
                "cargo_id": cargo_obj.id,
                "estadoVinculacion": estado_planta.id,
                "salario": planta_hist.salario or 0,
                "grado": planta_hist.grado or "",
                "resolucion": planta_hist.resolucion or "",
                "resolucion_archivo": None,
                "observacion": "Devolución a PLANTA (ocupante retirado)",
                "fechaInicio": hoy,
            }
            ser = CargoUsuarioSerializer(data=datos, context=context or {})
            ser.is_valid(raise_exception=True)
            nuevo_planta = ser.save()

            usuario.cargo = cargo_obj
            usuario.save(update_fields=["cargo"])

            # Recursivamente devolver ocupante retirado a su PLANTA
            devolver_a_planta(ocupante.usuario, visited=visited, context=context)
            return nuevo_planta