from .models import (
    Usuario, TipoCertificado, FormacionComplementaria,
    Bitacora, EstadoSolicitud, TipoSolicitud, Solicitud
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken



# -------------------------
# LOGIN PERSONALIZADO JWT
# -------------------------
class CustomTokenObtainPairSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        correo = attrs.get("correo")
        password = attrs.get("password")

        # 1️⃣ Buscar usuario en la base de datos
        try:
            user = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("❌ Credenciales inválidas")

        # 2️⃣ Verificar contraseña
        if not check_password(password, user.password):
            raise serializers.ValidationError("❌ Credenciales inválidas")

        # 3️⃣ Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # 4️⃣ Retornar datos y tokens
        return {
            "refresh": str(refresh),
            "access": str(access),
            "user_id": user.id,
            "nombre": user.nombre,
            "rol": user.rol.nombre,  # si quieres mostrar el nombre del rol
        }
# -------------------------
# SERIALIZADORES MODELOS
# -------------------------
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
            'password': {'write_only': True}  # para que no aparezca en GET
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)
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
