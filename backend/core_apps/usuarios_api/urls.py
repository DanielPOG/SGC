from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UsuarioViewSet,
    FormacionComplementariaViewSet,
    BitacoraViewSet,
    SolicitudViewSet,
    UsuarioView,
    CustomTokenObtainPairView,  # login personalizado
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'formaciones', FormacionComplementariaViewSet)
router.register(r'bitacoras', BitacoraViewSet)
router.register(r'solicitudes', SolicitudViewSet)

urlpatterns = [
    path("", include(router.urls)),

    # Login y refresh
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Perfil del usuario autenticado
    path("perfil/", UsuarioView.as_view(), name="usuario_perfil"),
]
