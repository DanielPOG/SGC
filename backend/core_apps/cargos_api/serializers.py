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

class CargoUsuarioSerializer(serializers.ModelSerializer):
    num_doc = serializers.CharField(write_only=True)

    class Meta:
        model = CargoUsuario
        fields = [
            "id", "cargo", "usuario", "num_doc",
            "estadoVinculacion", "salario", "grado",
            "resolucion", "resolucion_archivo",
            "observacion", "fechaInicio"
        ]
        extra_kwargs = {"usuario": {"read_only": True}}

    def _handle_logic(self, usuario, validated_data, instance=None):
        """
        Lógica de negocio completa:
        - Cierra cargos activos del usuario si inicia uno nuevo.
        - PLANTA: reemplaza titular anterior en el cargo.
        - TEMPORAL: pausa PLANTA si hay conflicto.
        - Retorno automático a PLANTA original cuando TEMPORAL termina.
        """
        hoy = timezone.now()
        cargo = validated_data["cargo"]
        estado = validated_data["estadoVinculacion"]

        # 1️⃣ Cerrar cargos activos del usuario si inicia uno nuevo
        activos = CargoUsuario.objects.filter(
            usuario=usuario,
            fechaRetiro__isnull=True
        )
        if instance:
            activos = activos.exclude(pk=instance.pk)

        for act in activos:
            if act.cargo != cargo or act.estadoVinculacion != estado:
                act.fechaRetiro = hoy
                act.save(update_fields=["fechaRetiro"])

        # 2️⃣ Si es PLANTA: cerrar titular anterior en el cargo y asignar nuevo
        if estado.estado.upper() == "PLANTA":
            titular_activo = CargoUsuario.objects.filter(
                cargo=cargo,
                estadoVinculacion__estado__iexact="PLANTA",
                fechaRetiro__isnull=True
            )
            if instance:
                titular_activo = titular_activo.exclude(pk=instance.pk)
            titular_activo = titular_activo.first()

            if titular_activo:
                titular_activo.fechaRetiro = hoy
                titular_activo.save(update_fields=["fechaRetiro"])
                titular_activo.usuario.cargo = None
                titular_activo.usuario.save(update_fields=["cargo"])

            usuario.cargo = cargo
            usuario.save(update_fields=["cargo"])

        # 3️⃣ Si es TEMPORAL: pausa cualquier PLANTA activa del usuario
        elif estado.estado.upper() == "TEMPORAL":
            planta_activa = CargoUsuario.objects.filter(
                usuario=usuario,
                estadoVinculacion__estado__iexact="PLANTA",
                fechaRetiro__isnull=True
            )
            if instance:
                planta_activa = planta_activa.exclude(pk=instance.pk)
            for p in planta_activa:
                p.fechaRetiro = hoy
                p.save(update_fields=["fechaRetiro"])

        # 4️⃣ Retorno automático a PLANTA original cuando TEMPORAL termina
        if instance and instance.estadoVinculacion.estado.upper() == "TEMPORAL":
            # Si se está cerrando un TEMPORAL
            if validated_data.get("fechaRetiro") and instance.fechaRetiro is None:
                # Reactivar PLANTA original si existe
                planta_original = CargoUsuario.objects.filter(
                    usuario=usuario,
                    estadoVinculacion__estado__iexact="PLANTA",
                    fechaRetiro__isnull=False
                ).order_by("-fechaRetiro").first()
                if planta_original:
                    planta_original.fechaRetiro = None
                    planta_original.save(update_fields=["fechaRetiro"])
                    usuario.cargo = planta_original.cargo
                    usuario.save(update_fields=["cargo"])

        return hoy

    def create(self, validated_data):
        num_doc = validated_data.pop("num_doc")

        try:
            usuario = Usuario.objects.get(num_doc=num_doc)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError(
                {"usuario": "No existe un usuario con ese documento"}
            )

        validated_data["usuario"] = usuario

        # Validación: TEMPORAL no puede ser asignado si cargo PLANTA ya está activo
        if validated_data["estadoVinculacion"].estado.upper() == "TEMPORAL":
            activo_planta = CargoUsuario.objects.filter(
                cargo=validated_data["cargo"],
                estadoVinculacion__estado__iexact="PLANTA",
                fechaRetiro__isnull=True
            ).first()
            if activo_planta:
                raise serializers.ValidationError(
                    {"cargo": f"No se puede asignar temporal. El cargo PLANTA ya está siendo cursado por {activo_planta.usuario.nombre}"}
                )

        validated_data["fechaInicio"] = self._handle_logic(usuario, validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        usuario = instance.usuario

        # Si se está cerrando un cargo (fechaRetiro)
        if "fechaRetiro" in validated_data and validated_data["fechaRetiro"] is not None:
            validated_data["fechaRetiro"] = validated_data.get("fechaRetiro")

        validated_data["fechaInicio"] = self._handle_logic(usuario, validated_data, instance=instance)
        return super().update(instance, validated_data)



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
