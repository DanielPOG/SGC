from rest_framework import viewsets, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Usuario, FormacionComplementaria, Bitacora, Solicitud
from .serializers import (
    UsuarioSerializer,
    FormacionComplementariaSerializer,
    BitacoraSerializer,
    SolicitudSerializer,
)


# ==============================
#   LOGIN CON CORREO
# ==============================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        correo = attrs.get("username")  # el frontend manda "username" como correo
        password = attrs.get("password")

        try:
            user = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"detail": "❌ Usuario o contraseña incorrectos"})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "❌ Usuario o contraseña incorrectos"})

        # SimpleJWT necesita el "username" interno
        attrs["username"] = user.username
        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ==============================
#   PERFIL DEL USUARIO
# ==============================
class UsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


# ==============================
#   CRUDs
# ==============================
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]


class FormacionComplementariaViewSet(viewsets.ModelViewSet):
    queryset = FormacionComplementaria.objects.all()
    serializer_class = FormacionComplementariaSerializer
    permission_classes = [permissions.IsAuthenticated]


class BitacoraViewSet(viewsets.ModelViewSet):
    queryset = Bitacora.objects.all()
    serializer_class = BitacoraSerializer
    permission_classes = [permissions.IsAuthenticated]


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [permissions.IsAuthenticated]
