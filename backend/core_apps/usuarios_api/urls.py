"""
  Usuario API urls
"""
from rest_framework_simplejwt.views import (
  TokenRefreshView
)
from rest_framework.routers import DefaultRouter, path
from .views import (
  UsuarioViewSet, FormacionComplementariaViewSet,
  BitacoraViewSet, SolicitudViewSet, PasswordRecoveringViewSet,
  LoginView
)

router = DefaultRouter()

router.register(r'usuario', UsuarioViewSet)
router.register(r'formaciones', FormacionComplementariaViewSet)
router.register(r'bitacoras', BitacoraViewSet)
router.register(r'solicitudes', SolicitudViewSet)
router.register(r'mail-check', PasswordRecoveringViewSet, basename='password-recover')

urlpatterns = router.urls + [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
