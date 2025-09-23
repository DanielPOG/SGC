from rest_framework import serializers
from core_apps.general.models import Area
from core_apps.usuarios_api.models import Usuario
from .models import  GrupoSena, UsuarioGrupo




class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ["id", "nombre"]


class UsuarioSimpleSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ["id", "nombre_completo", "correo"]

    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}".strip()


class GrupoSenaSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)
    area_id = serializers.PrimaryKeyRelatedField(
        queryset=Area.objects.all(), source="area", write_only=True
    )

    lider = UsuarioSimpleSerializer(read_only=True)
    lider_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), source="lider", write_only=True, allow_null=True
    )

    class Meta:
        model = GrupoSena
        fields = "__all__"
        read_only_fields = ("fecha_creacion",)


class UsuarioGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioGrupo
        fields = "__all__"
