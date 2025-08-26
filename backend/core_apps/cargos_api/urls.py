from rest_framework.routers import DefaultRouter
from .views import (
    CargoNombreViewSet,
    EstadoCargoViewSet,
    CargoViewSet,
    CargoFuncionViewSet,
    CargoUsuarioViewSet
)

router = DefaultRouter()
router.register(r'cargo-nombres', CargoNombreViewSet, basename='cargo-nombre')
router.register(r'estado-cargo', EstadoCargoViewSet, basename='estado-cargo')
router.register(r'cargos', CargoViewSet, basename='cargo')
router.register(r'cargo-funciones', CargoFuncionViewSet, basename='cargo-funcion')
router.register(r'cargo-usuarios', CargoUsuarioViewSet, basename='cargo-usuario')

urlpatterns = router.urls
