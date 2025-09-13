"""
    Serializadores de los modelos app cargos_api
"""
from rest_framework import serializers
from core_apps.general.models import Centro
from core_apps.usuarios_api.models import Usuario
from core_apps.usuarios_api.serializers import UsuarioSerializer
from .models import (
    CargoNombre, EstadoCargo, Cargo, CargoFuncion, CargoUsuario, Idp, EstadoVinculacion,
    IdpxCargo
)
from core_apps.general.views import CentroSerializer

class CargoNombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoNombre
        fields = '__all__'


class EstadoCargoSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstadoCargo
        fields = '__all__'

class IdpSerializer(serializers.ModelSerializer):
    queryset=Idp.objects.all(),
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

class EstadoVinculacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoVinculacion
        fields = '__all__'

class CargoFuncionSerializer(serializers.ModelSerializer):
    cargo = serializers.PrimaryKeyRelatedField(queryset=Cargo.objects.all())

    class Meta:
        model = CargoFuncion
        fields = '__all__'


class CargoUsuarioSerializer(serializers.ModelSerializer):
    cargo = serializers.PrimaryKeyRelatedField(queryset=Cargo.objects.all())
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = CargoUsuario
        fields = '__all__'

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
        slug_field="idp_id"
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

class IdpxCargoSerializer(serializers.ModelSerializer):
    idp_id = serializers.PrimaryKeyRelatedField(queryset=Idp.objects.all())
    cargo = serializers.PrimaryKeyRelatedField(queryset=Cargo.objects.all())

    idp_detalle = serializers.SerializerMethodField()
    cargo_detalle = serializers.SerializerMethodField()

    class Meta:
        model = IdpxCargo
        fields = '__all__'

    def get_idp_detalle(self, obj):
        return {
            "fechaCreacion": obj.idp.fechaCreacion,
            "numero": obj.idp.idp_id,  
            "estado": obj.idp.estado
        }

    def get_cargo_detalle(self, obj):
        return {
        "id": obj.cargo.id,
        "fechaCreacion": obj.cargo.fechaCreacion,
        "fechaActualizacion": obj.cargo.fechaActualizacion,
        "centro": getattr(obj.cargo.centro_id, "nombre", None),
        "cargoNombre": getattr(obj.cargo.cargoNombre_id, "nombre", None),
        "estadoCargo": getattr(obj.cargo.estadoCargo_id, "estado", None),
        }
