"""
    Serializers app users
"""
from rest_framework import serializers
from models import Usuarios, TiposDoc, Generos
from cargos.models import Cargos #pylint:disable=import-error
from formacion.models import EstudioFormal #pylint:disable=import-error
class TipoDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposDoc
        fields = ['id', 'tipo', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generos
        fields = ['id', 'sigla', 'nombre', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UsuarioSerializer(serializers.ModelSerializer):
    tipo_doc = TipoDocSerializer(read_only=True)
    genero = GeneroSerializer(read_only=True)
    cargo = serializers.PrimaryKeyRelatedField(queryset=Cargos.objects.all())
    estudio_formal = serializers.PrimaryKeyRelatedField(queryset=EstudioFormal.objects.all())
    class Meta:
        model = Usuarios
        fields = [
            'id', 'nombre', 'apellido', 'num_doc', 
            'tipo_doc', 'genero', 'correo', 
            'cargo', 'estudio_formal', 'fecha_ingreso',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
