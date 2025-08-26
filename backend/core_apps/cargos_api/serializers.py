"""
    Serializadores de los modelos app cargos_api
"""
from rest_framework import serializers
from core_apps.general.models import Centro
from core_apps.usuarios_api.models import Usuario
from .models import CargoNombre, EstadoCargo, Cargo, CargoFuncion, CargoUsuario


class CargoNombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoNombre
        fields = '__all__'


class EstadoCargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCargo
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    cargoNombre = serializers.PrimaryKeyRelatedField(queryset=CargoNombre.objects.all())
    estadoCargo = serializers.PrimaryKeyRelatedField(queryset=EstadoCargo.objects.all())
    centro = serializers.PrimaryKeyRelatedField(queryset=Centro.objects.all())

    class Meta:
        model = Cargo
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
