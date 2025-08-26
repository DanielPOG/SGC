from rest_framework import serializers
from .models import (
    TipoDocumento, Genero, EstudioFormal, Rol, Estado,
    Usuario, TipoCertificado, FormacionComplementaria,
    Bitacora, EstadoSolicitud, TipoSolicitud, Solicitud
)


# ===========================
# TIPOS Y CATÁLOGOS
# ===========================
class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = ('id', 'nombre', 'sigla')


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ('id', 'nombre', 'sigla')


class EstudioFormalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstudioFormal
        fields = ('id', 'nombre')


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id', 'nombre')


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ('id', 'nombre')


# ===========================
# USUARIO
# ===========================
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


# ===========================
# CERTIFICADOS Y FORMACIÓN
# ===========================
class TipoCertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCertificado
        fields = ('id', 'nombre')


class FormacionComplementariaSerializer(serializers.ModelSerializer):
    tipo = serializers.PrimaryKeyRelatedField(queryset=TipoCertificado.objects.all()) #pylint:disable=no-member
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = FormacionComplementaria
        fields = (
            'id', 'nombre', 'tipo', 'institucion',
            'fechaInicio', 'fechaFin', 'certificado', 'usuario'
        )


# ===========================
# BITÁCORA
# ===========================
class BitacoraSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = Bitacora
        fields = ('id', 'usuario', 'accion', 'fecha')
        read_only_fields = ('fecha',)


# ===========================
# SOLICITUDES
# ===========================
class EstadoSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoSolicitud
        fields = ('id', 'nombre')


class TipoSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSolicitud
        fields = ('id', 'nombre')


class SolicitudSerializer(serializers.ModelSerializer):
    emisor = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    receptor = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    tipo = serializers.PrimaryKeyRelatedField(queryset=TipoSolicitud.objects.all())#pylint:disable=no-member
    estado = serializers.PrimaryKeyRelatedField(queryset=EstadoSolicitud.objects.all())#pylint:disable=no-member

    class Meta:
        model = Solicitud
        fields = (
            'id', 'emisor', 'receptor', 'descripcion',
            'tipo', 'fechaCreacion', 'fechaAprovada', 'estado'
        )
        read_only_fields = ('fechaCreacion',)
