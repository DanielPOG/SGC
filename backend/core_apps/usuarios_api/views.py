from rest_framework import viewsets, permissions
from .models import Usuario, FormacionComplementaria, Bitacora, Solicitud
from .serializers import UsuarioSerializer, FormacionComplementariaSerializer, BitacoraSerializer, SolicitudSerializer


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
