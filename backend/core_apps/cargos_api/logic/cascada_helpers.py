# ------------------------------------------------------------
# File: core_apps/cargos_api/logic/cascada_helpers.py
# ------------------------------------------------------------
from typing import Optional, Set
from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import ValidationError as DRFValidationError


from core_apps.cargos_api.models import CargoUsuario, EstadoVinculacion, Cargo
from core_apps.usuarios_api.models import Usuario
from core_apps.cargos_api.serializers import CargoUsuarioSerializer


def devolver_a_planta(
    usuario: Usuario,
    visited: Optional[Set[int]] = None,
    context: Optional[dict] = None
):
    """
    Devuelve a un usuario a su último cargo PLANTA conocido.
    - Usa siempre el archivo histórico.
    """

    if visited is None:
        visited = set()

    if usuario.pk in visited:
        return None
    visited.add(usuario.pk)

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

    ya_tiene_planta = CargoUsuario.objects.filter(
        usuario=usuario,
        cargo=cargo_obj,
        estadoVinculacion=estado_planta,
        fechaRetiro__isnull=True
    ).exists()
    if ya_tiene_planta:
        return None

    ocupante = CargoUsuario.objects.filter(
        cargo=cargo_obj,
        fechaRetiro__isnull=True
    ).exclude(usuario=usuario).select_related("usuario").first()

    hoy = timezone.now()

    with transaction.atomic():
        datos = {
            "num_doc": usuario.num_doc,
            "cargo_id": cargo_obj.id,
            "estadoVinculacion": estado_planta.id,
            "salario": planta_hist.salario or 0,
            "grado": planta_hist.grado or "",
            "resolucion": planta_hist.resolucion or "",
            "resolucion_archivo": planta_hist.resolucion_archivo,  # 👈 siempre histórico
            "observacion": "Devolución a PLANTA",
            "fechaInicio": hoy,
        }
        ser = CargoUsuarioSerializer(data=datos, context=context or {})
        ser.is_valid(raise_exception=True)
        nuevo = ser.save()

        usuario.cargo = cargo_obj
        usuario.save(update_fields=["cargo"])

        if ocupante:
            ocupante.fechaRetiro = hoy
            ocupante.save(update_fields=["fechaRetiro"])
            devolver_a_planta(ocupante.usuario, visited=visited, context=context)

        return nuevo


def devolver_a_temporal(
    usuario: Usuario,
    cargo_destino: Cargo,
    resolucion_archivo,
    context: Optional[dict] = None
):
    """
    Devuelve a un usuario a un cargo TEMPORAL.
    - El archivo de resolución es obligatorio y siempre debe venir del frontend.
    - Nunca usa histórico.
    """

    if not resolucion_archivo:
        raise DRFValidationError("El archivo de resolución es obligatorio para TEMPORAL")

    try:
        estado_temp = EstadoVinculacion.objects.get(estado__iexact="TEMPORAL")
    except EstadoVinculacion.DoesNotExist:
        raise DRFValidationError("No existe EstadoVinculacion 'TEMPORAL'")

    hoy = timezone.now()

    datos = {
        "num_doc": usuario.num_doc,
        "cargo_id": cargo_destino.id,
        "estadoVinculacion": estado_temp.id,
        "salario": 0,
        "grado": "",
        "resolucion": "",
        "resolucion_archivo": resolucion_archivo,  # 👈 obligatorio desde frontend
        "observacion": "Devolución a TEMPORAL",
        "fechaInicio": hoy,
    }

    ser = CargoUsuarioSerializer(data=datos, context=context or {})
    ser.is_valid(raise_exception=True)
    nuevo_temp = ser.save()

    usuario.cargo = cargo_destino
    usuario.save(update_fields=["cargo"])

    return nuevo_temp