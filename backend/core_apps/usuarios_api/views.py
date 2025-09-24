from rest_framework import viewsets, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Usuario, FormacionComplementaria, Bitacora, Solicitud
from .serializers import (
    UsuarioSerializer,
    FormacionComplementariaSerializer,
    BitacoraSerializer,
    SolicitudSerializer,
    # Importamos el serializador desde el archivo serializers.py
    CustomTokenObtainPairSerializer, 
)


# ==============================
#   LOGIN CON CORREO
# ==============================
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para el login.
    Usa el serializador personalizado para autenticar con correo y password.
    """
    serializer_class = CustomTokenObtainPairSerializer


# ==============================
#   PERFIL DEL USUARIO
# ==============================
class UsuarioView(APIView):
    """
    Vista para obtener el perfil del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


# ==============================
#   CRUDs (Conjuntos de vistas)
# ==============================
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    Conjunto de vistas para operaciones CRUD sobre el modelo Usuario.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]


class FormacionComplementariaViewSet(viewsets.ModelViewSet):
    """
    Conjunto de vistas para operaciones CRUD sobre la FormacionComplementaria.
    """
    queryset = FormacionComplementaria.objects.all()
    serializer_class = FormacionComplementariaSerializer
    permission_classes = [permissions.IsAuthenticated]


class BitacoraViewSet(viewsets.ModelViewSet):
    """
    Conjunto de vistas para operaciones CRUD sobre el modelo Bitacora.
    """
    queryset = Bitacora.objects.all()
    serializer_class = BitacoraSerializer
    permission_classes = [permissions.IsAuthenticated]


class SolicitudViewSet(viewsets.ModelViewSet):
    """
    Conjunto de vistas para operaciones CRUD sobre el modelo Solicitud.
    """
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [permissions.IsAuthenticated]