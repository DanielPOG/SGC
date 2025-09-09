"""
    Serializadores de los modelos app cargos_api
"""
from rest_framework import serializers
from core_apps.general.models import Centro
from core_apps.usuarios_api.models import Usuario
from core_apps.usuarios_api.serializers import UsuarioSerializer
from .models import CargoNombre, EstadoCargo, Cargo, CargoUsuario, Idp, EstadoVinculacion
from core_apps.general.views import CentroSerializer
from django.utils import timezone


from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError as DRFValidationError
from core_apps.cargos_api.models import EstadoVinculacion

class CargoNombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoNombre
        fields = '__all__'


class EstadoCargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCargo
        fields = '__all__'
class EstadoVinculacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoVinculacion
        fields = '__all__'
        
class IdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idp
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    cargoNombre = serializers.PrimaryKeyRelatedField(queryset= CargoNombre.objects.all())
    estadoCargo = serializers.PrimaryKeyRelatedField(queryset= EstadoCargo.objects.all())
    centro = serializers.PrimaryKeyRelatedField(queryset= Centro.objects.all())
    idp = serializers.PrimaryKeyRelatedField(queryset= Idp.objects.all())
    fechaActualizacion = serializers.DateTimeField(read_only=True) 
    class Meta:
        model = Cargo
        fields = '__all__'

from rest_framework import serializers
class PayloadRootSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    cargo_id = serializers.IntegerField()  # 👈 usar cargo_id, no cargo
    num_doc = serializers.CharField()
    estadoVinculacion = serializers.IntegerField()
    salario = serializers.DecimalField(max_digits=10, decimal_places=2)
    grado = serializers.CharField()
    resolucion = serializers.CharField()
    resolucion_archivo = serializers.FileField(required=False, allow_null=True)  # 👈 ahora archivo real
    observacion = serializers.CharField(allow_blank=True, required=False)
    fechaInicio = serializers.DateField()
    fechaRetiro = serializers.DateField(allow_null=True, required=False)

from rest_framework import serializers
import json

class ConfirmacionCascadaSerializer(serializers.Serializer):
    root_usuario_id = serializers.IntegerField()
    cargo_destino_id = serializers.IntegerField()
    decisiones = serializers.ListField(child=serializers.DictField(), required=False)
    payload_root = serializers.DictField(required=False)
    resolucion_archivo = serializers.FileField(required=False, allow_null=True)

    def to_internal_value(self, data):
        """
        Convierte campos JSON que vienen como string desde FormData
        """
        ret = super().to_internal_value(data)

        # parsear payload_root si viene como string
        if "payload_root" in data and isinstance(data["payload_root"], str):
            try:
                ret["payload_root"] = json.loads(data["payload_root"])
            except json.JSONDecodeError:
                self.fail("invalid", field_name="payload_root")

        # parsear decisiones si vienen como string
        if "decisiones" in data and isinstance(data["decisiones"], str):
            try:
                ret["decisiones"] = json.loads(data["decisiones"])
            except json.JSONDecodeError:
                self.fail("invalid", field_name="decisiones")

        return ret


from rest_framework import serializers
from django.utils import timezone
from rest_framework.exceptions import ValidationError as DRFValidationError

from core_apps.usuarios_api.models import Usuario

class CargoUsuarioSerializer(serializers.ModelSerializer):
    # Para asignar usuario desde el frontend usando num_doc
    num_doc = serializers.CharField(write_only=True, required=True)

    # Para asignar cargo desde el frontend con el ID
    cargo_id = serializers.PrimaryKeyRelatedField(
        source="cargo", queryset=Cargo.objects.all(), required=True
    )

    # Para mostrar cargo como string (usa __str__ de Cargo)
    cargo = serializers.StringRelatedField(read_only=True)

    cargo_destino_id = serializers.IntegerField(required=False, allow_null=True)
    fechaRetiro = serializers.DateTimeField(required=False, allow_null=True)

    resolucion_archivo = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = CargoUsuario
        fields = [
            "id", "cargo", "cargo_id", "usuario", "num_doc", "cargo_destino_id",
            "estadoVinculacion", "salario", "grado",
            "resolucion", "resolucion_archivo",
            "observacion", "fechaInicio", "fechaRetiro"
        ]
        extra_kwargs = {"usuario": {"read_only": True}}

    def create(self, validated_data):
        num_doc = validated_data.pop("num_doc", None)
        cargo_destino_id = validated_data.pop("cargo_destino_id", None)
        self.context["cargo_destino_id"] = cargo_destino_id

        # Buscar usuario por documento
        if not num_doc:
            raise serializers.ValidationError({"num_doc": "Este campo es obligatorio"})
        try:
            usuario = Usuario.objects.get(num_doc=num_doc)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"usuario": "No existe un usuario con ese documento"})

        validated_data["usuario"] = usuario

        # Si no viene fechaInicio, usar ahora
        validated_data.setdefault("fechaInicio", timezone.now())

        # Validación: no permitir TEMPORAL si ya hay PLANTA activo en ese cargo
        estado_vinc = validated_data.get("estadoVinculacion")
        if estado_vinc and getattr(estado_vinc, "estado", "").upper() == "TEMPORAL":
            activo_planta = CargoUsuario.objects.filter(
                cargo=validated_data["cargo"],
                estadoVinculacion__estado__iexact="PLANTA",
                fechaRetiro__isnull=True
            ).first()
            if activo_planta:
                raise serializers.ValidationError(
                    {"cargo": f"No se puede asignar temporal. El cargo PLANTA ya está siendo cursado por {activo_planta.usuario.nombre}"}
                )

        instance = super().create(validated_data)
        self._post_create_update_logic(instance)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self._post_create_update_logic(instance, validated_data=validated_data)
        return instance

    def _post_create_update_logic(self, instance, validated_data=None):
        hoy = timezone.now()
        usuario = instance.usuario
        cargo = instance.cargo
        estado = getattr(instance.estadoVinculacion, "estado", "").upper()

        # cerrar cargos abiertos del usuario
        abiertos = CargoUsuario.objects.filter(
            usuario=usuario, fechaRetiro__isnull=True
        ).exclude(pk=instance.pk)
        for abierto in abiertos:
            abierto.fechaRetiro = hoy
            abierto.save(update_fields=["fechaRetiro"])

        if estado == "PLANTA":
            # cerrar otros en el mismo cargo
            titulares = CargoUsuario.objects.filter(
                cargo=cargo, fechaRetiro__isnull=True
            ).exclude(pk=instance.pk)
            for titular in titulares:
                titular.fechaRetiro = hoy
                titular.save(update_fields=["fechaRetiro"])

                if titular.estadoVinculacion.estado.upper() == "PLANTA":
                    titular.usuario.cargo = None
                    titular.usuario.save(update_fields=["cargo"])
                elif titular.estadoVinculacion.estado.upper() == "TEMPORAL":
                    from core_apps.cargos_api.logic.cascada_helpers import devolver_a_planta
                    devolver_a_planta(titular.usuario, visited=None, context=self.context)

            # resetear último planta para no dejar huella
            ultimo_planta = CargoUsuario.objects.filter(
                cargo=cargo, estadoVinculacion__estado__iexact="PLANTA"
            ).exclude(usuario=usuario).order_by("-fechaInicio").first()
            if ultimo_planta:
                ultimo_planta.usuario.cargo = None
                ultimo_planta.usuario.save(update_fields=["cargo"])

            usuario.cargo = cargo
            usuario.save(update_fields=["cargo"])

        elif estado == "TEMPORAL":
            planta_activa = CargoUsuario.objects.filter(
                usuario=usuario, estadoVinculacion__estado__iexact="PLANTA", fechaRetiro__isnull=True
            ).exclude(pk=instance.pk)
            for p in planta_activa:
                p.fechaRetiro = hoy
                p.save(update_fields=["fechaRetiro"])
                p.usuario.cargo = None
                p.usuario.save(update_fields=["cargo"])

        # cascada si se cierra temporal
        if estado == "TEMPORAL" and instance.fechaRetiro is not None:
            from core_apps.cargos_api.logic.cascada_helpers import devolver_a_planta
            devolver_a_planta(usuario, visited=None, context=self.context)


class CargoExcelSerializer(serializers.ModelSerializer):
    cargoNombre = serializers.SlugRelatedField(
        queryset=CargoNombre.objects.all(),
        slug_field="nombre"
    )
    estadoCargo = serializers.SlugRelatedField(
        queryset=EstadoCargo.objects.all(),
        slug_field="estado"
    )
    centro = serializers.SlugRelatedField(
        queryset=Centro.objects.all(),
        slug_field="nombre"
    )
    idp = serializers.SlugRelatedField(
        queryset=Idp.objects.all(),
        slug_field="numero"
    )

    class Meta:
        model = Cargo
        fields = '__all__'


# Serializer anidado (para lectura: GET list y retrieve)
class CargoNestedSerializer(serializers.ModelSerializer): #sirve para mostrar los detalles del cargo
    cargoNombre = CargoNombreSerializer(read_only=True)
    estadoCargo = EstadoCargoSerializer(read_only=True)
    centro = CentroSerializer(read_only=True)
    idp = IdpSerializer(read_only=True)
    fechaCreacion = serializers.DateTimeField(read_only=True)
    fechaActualizacion = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Cargo
        fields = "__all__"

class CargoUsuarioNestedSerializer(serializers.ModelSerializer):
    cargo = CargoNestedSerializer(read_only=True)  
    usuario = UsuarioSerializer(read_only=True)    
    estado = EstadoCargoSerializer(read_only=True)
    class Meta:
        model = CargoUsuario
        fields = '__all__'






# Serializer simple para devolver lo creado
class CargoUsuarioSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoUsuario
        fields = [
            "id", "usuario", "cargo", "estadoVinculacion",
            "fechaInicio", "fechaRetiro", "salario", "grado", "resolucion"
        ]


class SimulacionInputSerializer(serializers.Serializer):
    root_usuario_id = serializers.IntegerField()


class DecisionItemSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    cargo_id = serializers.IntegerField()
    tipo = serializers.ChoiceField(choices=["planta", "temporal"])


class ConfirmacionCascadaSerializer(serializers.Serializer):
    root_usuario_id = serializers.IntegerField()
    decisiones = DecisionItemSerializer(many=True)
