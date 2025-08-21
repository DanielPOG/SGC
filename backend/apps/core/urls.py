from django.urls import path, include
from rest_framework_nested import routers
from .views import CentrosViewSet,RegionalesViewSet,EstadosViewSet #pylint:disable=relative-beyond-top-level

router = routers.DefaultRouter()
router.register(r'centro', CentrosViewSet)
router.register(r'regional', RegionalesViewSet)
router.register(r'estado', EstadosViewSet)

regional_router = routers.NestedDefaultRouter(router, r'regional', lookup="regional")
regional_router.register(r'centro', CentrosViewSet, basename='regional-centro')

centro_router = routers.NestedDefaultRouter(router, r'centro', lookup="centro")
centro_router.register(r'regional', RegionalesViewSet, basename='centro-regional')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(regional_router.urls)),
    path('', include(centro_router.urls))
]
