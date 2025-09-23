from rest_framework import serializers
from .models import Regional, Centro, Red, Area, Dependencia


class RegionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regional
        fields = '__all__'


class CentroSerializer(serializers.ModelSerializer):
    regional = RegionalSerializer(read_only=True)

    class Meta:
        model = Centro
        fields = "__all__"


class RedSerializer(serializers.ModelSerializer):
    centro = serializers.PrimaryKeyRelatedField(queryset=Centro.objects.all())

    class Meta:
        model = Red
        fields = ['id', 'codigoRed', 'nombre', 'centro']


class AreaSerializer(serializers.ModelSerializer):
    red = serializers.PrimaryKeyRelatedField(queryset=Red.objects.all())

    class Meta:
        model = Area
        fields = ['id', 'codigoArea', 'nombre', 'red']


class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = ['id', 'codigoDependencia', 'nombre']
