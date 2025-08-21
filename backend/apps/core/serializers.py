"""
    core models serializers
"""
from rest_framework import serializers
from apps.core.models import Estados, Regionales, Centros #pylint:disable=import-error

class EstadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estados
        fields = ['id', 'nombre']

class RegionalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regionales
        fields = ['id', 'nombre']

class CentrosSerializer(serializers.ModelSerializer):
    regional = serializers.PrimaryKeyRelatedField(queryset=Regionales.objects.all())
    class Meta:
        model = Centros
        fields = ['id','nombre', 'regional']