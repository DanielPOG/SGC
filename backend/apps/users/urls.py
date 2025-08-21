from django.urls import path, include
from rest_framework_nested import routers
from .views import UsuarioViewSet, TipoDocViewSet, GeneroViewSet#pylint: disable=relative-beyond-top-level

router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet)
router.register('')
