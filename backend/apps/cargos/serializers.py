"""
    Serializadores modelos de app cargos 
"""
from rest_framework import serializers
from .models import NombresCargo, Cargos, UsuariosCargo#pylint: disable=relative-beyond-top-level
from apps.users.models import Usuarios #pylint:disable=import-error 
from apps.core.serializers import EstadosSerializer #pylint:disable=import-error
class NombresSerializer(serializers.ModelSerializer):
    class Meta:
        model=NombresCargo
        fields=['id','nombre']

class CargosSerializer(serializers.ModelSerializer):
    estado = EstadosSerializer(read_only=True)
    nombre = NombresSerializer(read_only=True)
    class Meta:
        model=Cargos
        fields=['id', 'idp', 'resolucion', 'nombre', 'estado', 'created_at', 'updated_at']
        read_only_fields=['id','created_at', 'updated_at']

class UsuariosCargoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuarios.objects.all())
    cargo = CargosSerializer(read_only=True)
    class Meta:
        model=UsuariosCargo
        fields=['id','cargo','usuario','fecha_asignacion','fecha_fin','grado',
                'created_at','updated_at']
        read_only_fields=['id', 'created_at', 'updated_at']
