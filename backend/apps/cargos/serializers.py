"""
    Serializadores modelos de app cargos 
"""
from rest_framework import serializers
from .models import NombresCargo, Cargos, UsuariosCargo#pylint: disable=relative-beyond-top-level
from apps.users.models import Usuarios #pylint:disable=import-error 
from apps.core.models import Estados #pylint:disable=import-error
class NombresSerializer(serializers.ModelSerializer):
    class Meta:
        model=NombresCargo
        fields=['id','nombre']

class CargosSerializer(serializers.ModelSerializer):
    estado = serializers.SlugRelatedField(
        slug_field="id",  # campo del modelo relacionado
        queryset=Estados.objects.all()
    )
    nombre = serializers.SlugRelatedField(
        slug_field ="id",
        queryset=NombresCargo.objects.all()
    )
    class Meta:
        model=Cargos
        fields='__all__'
        read_only_fields=['id','created_at', 'updated_at']



class UsuariosCargoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuarios.objects.all())
    cargo = CargosSerializer(read_only=True)
    # genero = serializers.SlugRelatedField(
    #     slug_field="id",
    #     queryset=Generos.objects.all()
    # )
    # tipo_doc = serializers.SlugRelatedField(
    #     slug_field="id",
    #     queryset=TiposDoc.objects.all()
    # )
    class Meta:
        model=UsuariosCargo
        fields='__all__'
        read_only_fields=['id', 'created_at', 'updated_at']
