"""
    Serializadores modelos de app "formacion"
"""
from rest_framework import serializers
from models import EstudioFormal, Complementaria
from users.models import Usuarios # pylint: disable=import-error

class FormalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstudioFormal
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class ComplementariaSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuarios.objects.all())
    class Meta:
        model=Complementaria
        fields=['id','tipo','usuario','institucion','certificado','fecha_inicio','fecha_fin']
        read_only_fields = ['id', 'fecha_inicio', 'fecha_fin']
