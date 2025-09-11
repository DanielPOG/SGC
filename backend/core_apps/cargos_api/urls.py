from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    CargoNombreViewSet,
    EstadoCargoViewSet,
    CargoViewSet,
    CargoUsuarioViewSet,
    CargoUploadView,
    IdpViewSet
)

router = DefaultRouter()
router.register(r'cargo-nombres', CargoNombreViewSet, basename='cargo-nombre')
router.register(r'estado-cargo', EstadoCargoViewSet, basename='estado-cargo')
router.register(r'cargos', CargoViewSet, basename='cargo')
router.register(r'cargo-usuarios', CargoUsuarioViewSet, basename='cargo-usuario')
router.register(r'idps', IdpViewSet, basename='idp')
# Aquí defines las URL manuales
custom_urls = [
    path('upload/', CargoUploadView.as_view(), name='cargo-upload'),
]
urlpatterns = router.urls + custom_urls
