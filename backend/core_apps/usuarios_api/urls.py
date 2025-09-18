from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, FormacionComplementariaViewSet, BitacoraViewSet, SolicitudViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'formaciones', FormacionComplementariaViewSet)
router.register(r'bitacoras', BitacoraViewSet)
router.register(r'solicitudes', SolicitudViewSet)

urlpatterns = router.urls
