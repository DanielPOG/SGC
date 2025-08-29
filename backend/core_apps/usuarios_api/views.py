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

class PasswordRecovering(APIView):
    def get(request):
        email = request.query_params.get('email')
        exists = Usuario.objects.filter(correo=email).first()
        if not exists:
            return Response({'error':'Usuario no encontrado', 'exists':False}, status=404)
        return Response({'msg':'Correo Confirmado', 'exists':True})
    def post(request):
        email = request.data.get("email")
        oldPassword = request.data.get("old_password")
        newPassword = request.data.get("new_password")
        DBOldPassword = Usuario.objects.filter(correo=email).get(password=oldPassword)
        if not DBOldPassword:
            return
    


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
