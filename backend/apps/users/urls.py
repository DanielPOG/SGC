from django.urls import path, include
from rest_framework_nested import routers
from .views import UsuarioViewSet, TipoDocViewSet, GeneroViewSet#pylint: disable=relative-beyond-top-level

router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet)
router.register(r'tipo-doc', TipoDocViewSet)
router.register(r'genero', GeneroViewSet)

usuario_router = routers.NestedDefaultRouter(router, r'usuario', lookup='usuario')
usuario_router.register(r'tipo-doc', TipoDocViewSet, basename="usuario-tipo-doc")
usuario_router.register(r'genero', GeneroViewSet, basename="usuario-genero")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(usuario_router.urls))
]
