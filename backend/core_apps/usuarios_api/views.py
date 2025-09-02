from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Usuario, FormacionComplementaria, Bitacora, Solicitud
from .serializers import UsuarioSerializer, FormacionComplementariaSerializer, BitacoraSerializer, SolicitudSerializer

#APIVIEW PENDIENTE
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

class PasswordRecovering(viewsets.ViewSet):
    def get(self, request):
        """
            Verificar si el correo institucional existe en la base de datos
        """
        email = request.query_params.get('email')
        exists = Usuario.objects.filter(correo=email).first()
        if not exists:
            return Response({'error':'Usuario no encontrado'}, status=404)
        return Response({'msg':'Correo Confirmado'}, status=status.HTTP_200_OK)
    def post(self, request):
        """
            Verificar
        """
        email = request.data.get("email")
        newPassword = request.data.get("new_password")
        try:
            usuario = Usuario.objects.filter(correo=email)
        except Usuario.DoesNotExist:
            return Response({'error':'Usuario no encontrado'})    


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
