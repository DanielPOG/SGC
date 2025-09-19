from rest_framework import serializers
from .models import (
    Autorizacion, Permiso, PermisosUsuario, Usuario, TipoCertificado, FormacionComplementaria,
    Bitacora, EstadoSolicitud, TipoSolicitud, Solicitud
)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        depth =2
        model = Usuario
        fields = (
            'id', 'nombre', 'apellido', 'num_doc', 'tipo_doc',
            'correo', 'password', 'genero', 'cargo', 'estudioF',
            'fechaInicio', 'fechaActualizacion', 'fechaRetiro',
            'rol', 'fecha_n', 'resolucion', 'estado', 'dependencia',
            'software', 'is_active', 'is_staff', 'is_superuser'
        )
        extra_kwargs = {
            'password': {'write_only': True}  # <- para que no aparezca en GET
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)  # <- asegura que se encripte
        user.save()
        return user

class FormacionComplementariaSerializer(serializers.ModelSerializer):
    tipo = serializers.PrimaryKeyRelatedField(queryset=TipoCertificado.objects.all()) 
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = FormacionComplementaria
        fields = (
            'id', 'nombre', 'tipo', 'institucion',
            'fechaInicio', 'fechaFin', 'certificado', 'usuario'
        )


class BitacoraSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = Bitacora
        fields = ('id', 'usuario', 'accion', 'fecha')
        read_only_fields = ('fecha',)


class SolicitudSerializer(serializers.ModelSerializer):
    emisor = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    receptor = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    tipo = serializers.PrimaryKeyRelatedField(queryset=TipoSolicitud.objects.all())
    estado = serializers.PrimaryKeyRelatedField(queryset=EstadoSolicitud.objects.all())

    class Meta:
        model = Solicitud
        fields = (
            'id', 'emisor', 'receptor', 'descripcion',
            'tipo', 'fechaCreacion', 'fechaAprovada', 'estado'
        )
        read_only_fields = ('fechaCreacion',)
class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['id', 'nombre', 'codigo']


class AuthSerializer(serializers.ModelSerializer):
    permisos = PermisoSerializer(many=True, read_only=True)

    class Meta:
        model = Autorizacion
        fields = ['id', 'nombre', 'permisos']


class PermisoUsuarioSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)  # Muestra correo o __str__ de Usuario
    permiso = PermisoSerializer(read_only=True)

    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(),
        source="usuario",
        write_only=True
    )
    permiso_id = serializers.PrimaryKeyRelatedField(
        queryset=Permiso.objects.all(),
        source="permiso",
        write_only=True
    )

    class Meta:
        model = PermisosUsuario
        fields = ['id', 'usuario', 'permiso', 'usuario_id', 'permiso_id', 'otorgado_en']