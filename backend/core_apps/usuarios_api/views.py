"""
    Vistas de la api usuarios, todas las funciones de inicio y recuperacion estan aqui
"""
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import (viewsets, permissions, status)
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, action #pylint:disable=unused-import
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import (
    Usuario, FormacionComplementaria, Bitacora, Solicitud,
    PermisosUsuario, Permiso, Autorizacion
) 
from .serializers import (
    UsuarioSerializer, FormacionComplementariaSerializer,
    BitacoraSerializer, SolicitudSerializer, PermisoUsuarioSerializer,
    PermisoSerializer, AuthSerializer
)

class LoginView(TokenObtainPairView):
    """
        Vista extendida sin JWT-Auth para iniciar sesión
    """
    permission_classes = [AllowAny]

#APIVIEW PENDIENTE
class UsuarioViewSet(viewsets.ModelViewSet):
    """
        Viewset de usuario
    """
    queryset = (Usuario.objects.select_related(
            "tipo_doc","genero","cargo","estudioF","rol","estado","dependencia",
            "cargo__cargoNombre","cargo__idp","cargo__estadoCargo","cargo__centro"
        ))
    serializer_class = UsuarioSerializer
    @action(methods=['get'], detail=False)
    def cargarUsers(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    #permission_classes = [permissions.IsAuthenticated]

class PasswordRecoveringViewSet(viewsets.ViewSet):
    """
        Viewset modulo recuperar contraseña
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    @action(detail=False, methods=['get'])
    def send_recovering_mail(self, request):
        """
            Metodo para enviar correo de recuperación de contraseña al funcionario
        """
        email = request.query_params.get('email')
        if not Usuario.objects.filter(correo=email).exists():
            return Response({"error":"Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        subject = "Recuperación de contraseña"
        message = (f'Haz clic en este enlace para reestablecer tu contraseña:\n'
                f'http://localhost:3000/reset-password?email={email}')
        from_email = None #Usa el DEFAULT_FROM_EMAIL
        recipient_list = [email]
        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({"msg":"Correo de recuperación enviado."}, status=status.HTTP_200_OK)
        except Exception as err: #pylint:disable=broad-exception-caught
            return Response({"error":str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def pass_reset(self, request):
        """
            Formatear la contraseña
        """
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        try:
            usuario = Usuario.objects.filter(correo=email)
        except Usuario.DoesNotExist: #pylint:disable=no-member
            return Response({'error':'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        usuario.set_password(new_password)
        usuario.save()
        return Response({'msg':'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)

class FormacionComplementariaViewSet(viewsets.ModelViewSet):
    """
        a
    """
    queryset = FormacionComplementaria.objects.all() #pylint:disable=no-member
    serializer_class = FormacionComplementariaSerializer
    permission_classes = [permissions.IsAuthenticated]


class BitacoraViewSet(viewsets.ModelViewSet):
    """
        a
    """
    queryset = Bitacora.objects.all() #pylint:disable=no-member
    serializer_class = BitacoraSerializer
    permission_classes = [permissions.IsAuthenticated]


class SolicitudViewSet(viewsets.ModelViewSet):
    """
        a
    """
    queryset = Solicitud.objects.all() #pylint:disable=no-member
    serializer_class = SolicitudSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermisoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PermisosUsuario.objects.all() #pylint:disable=no-member
    serializer_class = PermisoUsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    @action(methods=['post'], detail=False)
    def crearPermisoUsuario(self, request):
        usuario_id = request.data.get('usuario_id')
        permiso_slug = request.data.get('slug')
        if not Permiso.objects.filter(codigo=permiso_slug).exists():
            return Response({'error':'Permiso no disponible.'})
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return Response({"error":"Hubo un error al dar permisos al usuario"})
        permiso = Permiso.objects.get(codigo=permiso_slug)
        if PermisosUsuario.objects.filter(usuario=usuario.id, permiso=permiso.id).exists():
            return Response({"error":f"Este usuario ya cuenta con este permiso"})
        permiso = PermisosUsuario(usuario=usuario.id, permiso=permiso.id)
        permiso.save()
        return Response({'msg':'Permiso Asignado'})