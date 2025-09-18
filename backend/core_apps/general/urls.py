from rest_framework.routers import DefaultRouter
from .views import (
    RegionalViewSet,
    CentroViewSet,
    RedViewSet,
    AreaViewSet,
    DependenciaViewSet
)

router = DefaultRouter()
router.register(r'regionales', RegionalViewSet, basename='regional')
router.register(r'centros', CentroViewSet, basename='centro')
router.register(r'redes', RedViewSet, basename='red')
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'dependencias', DependenciaViewSet, basename='dependencia')

urlpatterns = router.urls
