"""
    Serializadores modelos app "grupos"
"""
from rest_framework import serializers
from models import EstadosGrupo, Grupos, UsuariosGrupo
from core.models import Centros # pylint: disable=import-error
from users.models import Usuarios # pylint: disable=import-error

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model=EstadosGrupo
        fields = ['id', 'nombre', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class GrupoSerializer(serializers.ModelSerializer):
    centro = serializers.PrimaryKeyRelatedField(queryset=Centros.objects.all())
    estado = serializers.PrimaryKeyRelatedField(queryset=EstadosGrupo.objects.all())
    lider = serializers.PrimaryKeyRelatedField(queryset=Usuarios.objects.all())
    class Meta:
        model = Grupos
        fields = [
            'id', 'nombre', 'centro', 'estado', 'lider', 
            'resolucion', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class UsuarioGrupoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuarios.objects.all())
    grupo = serializers.PrimaryKeyRelatedField(queryset=Grupos.objects.all())
    class Meta:
        model = UsuariosGrupo
        fields = ['id', 'usuario', 'grupo', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
