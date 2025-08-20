from django.urls import path, include
from rest_framework_nested import routers
from views import CargosViewSet, NombresViewSet, UsuarioCargoViewSet

router = routers.DefaultRouter()
router.register(r'cargos', CargosViewSet)

cargos_router = routers.NestedDefaultRouter(router, r'cargos', lookup='cargo')
cargos_router.register(r'nombres', NombresViewSet, basename='cargo-nombres')
cargos_router.register(r'usuario', UsuarioCargoViewSet, basename='cargo-usuarios')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(cargos_router.urls))
]
