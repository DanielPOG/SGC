from core_apps.cargos_api.models import CargoUsuario, Cargo
from core_apps.usuarios_api.models import Usuario
from rest_framework.exceptions import ValidationError

def _planta_original(usuario: Usuario):
    """Devuelve el último registro PLANTA de un usuario."""
    return CargoUsuario.objects.filter(
        usuario=usuario,
        estadoVinculacion__estado__iexact="PLANTA"
    ).order_by("-fechaInicio").first()

def _cargos_libres():
    """Cargos sin un CargoUsuario activo."""
    return Cargo.objects.exclude(
        id__in=CargoUsuario.objects.filter(fechaRetiro__isnull=True).values_list("cargo_id", flat=True)
    )

def _temporal_activo_en_cargo(cargo: Cargo):
    """Si un cargo de planta tiene alguien ocupándolo temporalmente, devolverlo."""
    return CargoUsuario.objects.filter(
        cargo=cargo,
        estadoVinculacion__estado__iexact="TEMPORAL",
        fechaRetiro__isnull=True
    ).select_related("usuario").first()

def build_escalon_sugerencias(root_usuario_id: int, cargo_destino_id: int, tipo_decision: str):
    """
    Construye sugerencias escalonadas:
    - Planta → siempre apunta al cargo de planta original del usuario.
    - Temporales → lista de cargos libres.
    """
    try:
        root = Usuario.objects.get(pk=root_usuario_id)
    except Usuario.DoesNotExist:
        raise ValidationError("Usuario raíz no existe")

    sugerencias = []
    visited = set()

    def _rec(usuario: Usuario):
        if usuario.pk in visited:
            return
        visited.add(usuario.pk)

        ultimo_planta = _planta_original(usuario)
        if not ultimo_planta:
            return

        cargo_planta = ultimo_planta.cargo
        opciones = [{
            "cargo_id": cargo_planta.pk,
            "cargo_nombre": getattr(getattr(cargo_planta, "cargoNombre", None), "nombre", None),
            "tipo": "planta",
        }]

        for cargo in _cargos_libres():
            opciones.append({
                "cargo_id": cargo.pk,
                "cargo_nombre": getattr(getattr(cargo, "cargoNombre", None), "nombre", None),
                "tipo": "temporal",
            })

        sugerencias.append({
            "usuario_id": usuario.pk,
            "usuario_nombre": usuario.nombre,
            "num_doc": usuario.num_doc,
            "grado": ultimo_planta.grado,
            "salario": str(ultimo_planta.salario),
            "resolucion": ultimo_planta.resolucion,
            "estadoVinculacion": ultimo_planta.estadoVinculacion_id,
            "fechaInicio": ultimo_planta.fechaInicio.isoformat(),
            "observacion": ultimo_planta.observacion or "",
            "resolucion_archivo": ultimo_planta.resolucion_archivo.url if ultimo_planta.resolucion_archivo else None,
            "opciones": opciones,
        })

        temp_en_planta = _temporal_activo_en_cargo(cargo_planta)
        if temp_en_planta:
            _rec(temp_en_planta.usuario)

    if tipo_decision.lower() in ["planta", "temporal"]:
        _rec(root)

    return sugerencias

# --------------------------
# Aplicación de decisiones
# --------------------------
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from core_apps.cargos_api.models import  CargoUsuario, Cargo, EstadoVinculacion
from core_apps.cargos_api.serializers import CargoUsuarioSerializer
from django.core.exceptions import ObjectDoesNotExist

def _normalize_date(date_str):
    if not date_str:
        return None
    from datetime import datetime
    try:
        # Si viene solo YYYY-MM-DD → lo convertimos a datetime con hora 00:00:00
        return datetime.strptime(date_str[:10], "%Y-%m-%d")
    except Exception:
        return None


def aplicar_decisiones_cascada(root_usuario_id, cargo_destino_id, decisiones):
    """
    Aplica todas las decisiones de manera segura:
    - Usuarios nuevos y antiguos
    - Temporal y Planta
    - Archivos opcionales
    - Validaciones preventivas
    """
    resultados = []
    hoy = timezone.now()
    visited = set()

    if not isinstance(decisiones, list):
        raise serializers.ValidationError({"decisiones": "Debe ser una lista"})

    # Deduplicar por num_doc
    decisiones_por_doc = {}
    for d in decisiones:
        num_doc = d.get("num_doc")
        if not num_doc:
            raise serializers.ValidationError({"num_doc": "Obligatorio en cada decisión"})
        decisiones_por_doc[str(num_doc)] = d
    decisiones = list(decisiones_por_doc.values())

    with transaction.atomic():
        for d in decisiones:
            tipo = d.get("tipo")
            num_doc = str(d.get("num_doc"))

            if tipo not in ("planta", "temporal"):
                raise serializers.ValidationError({"tipo": f"Tipo desconocido: {tipo}"})

            # Campos obligatorios
            campos_obligatorios = ["estadoVinculacion", "salario", "grado", "resolucion", "fechaInicio"]
            faltantes = [c for c in campos_obligatorios if d.get(c) in (None, "")]
            if faltantes:
                raise serializers.ValidationError({
                    "detalle": f"Faltan campos en decisión {tipo} usuario {num_doc}: {', '.join(faltantes)}"
                })

            usuario, _ = Usuario.objects.get_or_create(num_doc=num_doc)

            if tipo == "planta":
                # Intentar tomar último PLANTA histórico
                ultimo_planta = CargoUsuario.objects.filter(
                    usuario=usuario, estadoVinculacion__estado__iexact="PLANTA"
                ).order_by("-fechaInicio").first()

                if ultimo_planta:
                    datos = {
                        "num_doc": num_doc,
                        "cargo_id": ultimo_planta.cargo.id,
                        "estadoVinculacion": ultimo_planta.estadoVinculacion.id,
                        "salario": ultimo_planta.salario,
                        "grado": ultimo_planta.grado,
                        "resolucion": ultimo_planta.resolucion,
                        "observacion": d.get("observacion") or "Reasignado por devolución escalonada",
                        "fechaInicio": _normalize_date(d.get("fechaInicio")) or ultimo_planta.fechaInicio,
                        "fechaRetiro": None,
                        "resolucion_archivo": d.get("resolucion_archivo"),
                    }
                    serializer = CargoUsuarioSerializer(data=datos)
                    serializer.is_valid(raise_exception=True)
                    instance = serializer.save()
                    usuario.cargo = instance.cargo
                    usuario.save(update_fields=["cargo"])
                    resultados.append(instance)

            else:  # temporal
                cargo_pk = d.get("cargo_id")
                if not cargo_pk:
                    raise serializers.ValidationError({"cargo_id": "Obligatorio para decisiones tipo 'temporal'"})

                datos = {
                    "num_doc": num_doc,
                    "cargo_id": int(cargo_pk),
                    "estadoVinculacion": d.get("estadoVinculacion"),
                    "salario": d.get("salario"),
                    "grado": d.get("grado"),
                    "resolucion": d.get("resolucion"),
                    "observacion": d.get("observacion", ""),
                    "fechaInicio": _normalize_date(d.get("fechaInicio")),
                    "fechaRetiro": _normalize_date(d.get("fechaRetiro")),
                    "resolucion_archivo": d.get("resolucion_archivo"),
                }
                serializer = CargoUsuarioSerializer(data=datos, context={"cargo_destino_id": cargo_destino_id})
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                usuario.cargo = instance.cargo
                usuario.save(update_fields=["cargo"])
                resultados.append(instance)

                # Si temporal con fechaRetiro, devolver a PLANTA
                if datos.get("fechaRetiro"):
                    devolver_a_planta(usuario, hoy=hoy, visited=visited, context={"cargo_destino_id": cargo_destino_id})

    return resultados