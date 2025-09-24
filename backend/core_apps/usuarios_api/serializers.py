from rest_framework import serializers
from .models import (
    Usuario, TipoCertificado, FormacionComplementaria,
    Bitacora, EstadoSolicitud, TipoSolicitud, Solicitud
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador de login personalizado.
    Usa correo como campo de autenticación.
    """
    username_field = "correo"  # <- cambiamos el campo de login

    def validate(self, attrs):
        correo = attrs.get("username")  # viene como "username" desde el cliente
        password = attrs.get("password")

        user = authenticate(correo=correo, password=password)

        if not user:
            raise serializers.ValidationError("❌ Credenciales inválidas")

        data = super().validate(attrs)
        data["user_id"] = self.user.id
        data["nombre"] = self.user.nombre
        data["rol"] = self.user.rol
        return data


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
            'password': {'write_only': True}
        }


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
