from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, FormacionComplementariaViewSet, BitacoraViewSet, SolicitudViewSet, PasswordRecovering

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'formaciones', FormacionComplementariaViewSet)
router.register(r'bitacoras', BitacoraViewSet)
router.register(r'solicitudes', SolicitudViewSet)
router.register(r'mail-check', PasswordRecovering, basename='password-recover')

urlpatterns = router.urls
