"""
    Serializadores de modelos app funcionarios
"""
from rest_framework import serializers
from models import Bitacoras, Red, Area
from users.models import Usuarios # pylint: disable=import-error
from core.models import Centros # pylint: disable=import-error
class BitacoraSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuarios.objects.all())
    class Meta:
        model=Bitacoras
        fields=['id', 'usuario', 'accion']
        read_only_fields = ['id', 'usuario']

class RedSerializer(serializers.ModelSerializer):
    centro = serializers.PrimaryKeyRelatedField(queryset=Centros.objects.all())
    class Meta:
        model=Red
        fields=['id', 'centro']

class AreaSerializer(serializers.ModelSerializer):
    red = serializers.PrimaryKeyRelatedField(queryset=Red.objects.all())
    class Meta:
        model= Area
        fields=['id', 'red']
