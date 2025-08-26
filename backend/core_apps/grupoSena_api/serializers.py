"""
    Serializers
"""
from core_apps.general.models import Centro
from core_apps.usuarios_api.models import Usuario
from core_apps.cargos_api.models import CargoUsuario
from rest_framework import serializers
from .models import EstadoGrupo, GrupoSena, UsuarioGrupo



class EstadoGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoGrupo
        fields = '__all__'


class GrupoSenaSerializer(serializers.ModelSerializer):
    centro = serializers.PrimaryKeyRelatedField(queryset=Centro.objects.all())#pylint:disable=no-member
    estadoGrupo = serializers.PrimaryKeyRelatedField(queryset=EstadoGrupo.objects.all())#pylint:disable=no-member
    lider = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = GrupoSena
        fields = '__all__'
        read_only_fields = ("fechaCreacion", "fechaActualizacion")


class UsuarioGrupoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    grupo = serializers.PrimaryKeyRelatedField(queryset=GrupoSena.objects.all())#pylint:disable=no-member
    usuarioxcargo = serializers.PrimaryKeyRelatedField(queryset=CargoUsuario.objects.all())#pylint:disable=no-member

    class Meta:
        model = UsuarioGrupo
        fields = '__all__'
