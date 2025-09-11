from rest_framework import serializers
from .models import (
    Usuario, TipoCertificado, FormacionComplementaria,
    Bitacora, EstadoSolicitud, TipoSolicitud, Solicitud,
    Autorizacion, Permiso, PermisosUsuario
)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
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

#    Autorizacion, Permiso, PermisosRol
class AuthSerializer(serializers.ModelSerializer):
    nombre=serializers.CharField()
    class Meta:
        fields = '__all__'
        model = Autorizacion

class PermisoSerializer(serializers.ModelSerializer):
    autorizacion = serializers.PrimaryKeyRelatedField(queryset=Autorizacion.objects.all())
    nombre=serializers.CharField()
    codigo= serializers.SlugField(allow_unicode=True)
    class Meta:
        fields = '__all__'
        model = Permiso

class PermisoxUsuarioSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    permiso = serializers.PrimaryKeyRelatedField(queryset=Permiso.objects.all())
    class Meta:
        fields = '__all__'
        model = PermisosUsuario
        read_only_fields = ('otorgado_en')
