from rest_framework.routers import DefaultRouter
from .views import EstadoGrupoViewSet, GrupoSenaViewSet, UsuarioGrupoViewSet

router = DefaultRouter()
router.register(r'estado-grupo', EstadoGrupoViewSet, basename='estado-grupo')
router.register(r'grupo-sena', GrupoSenaViewSet, basename='grupo-sena')
router.register(r'usuario-grupo', UsuarioGrupoViewSet, basename='usuario-grupo')

urlpatterns = router.urls
