from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudioFormalViewSet, EducacionComplementariaViewSet #pylint:disable=relative-beyond-top-level

router = DefaultRouter()
router.register(r'formacion/formal', EstudioFormalViewSet, basename="formacion-formal")
router.register(
    r'formacion/complementaria', 
    EducacionComplementariaViewSet,
    basename="formacion-complementaria"
)

urlpatterns = [
    path('', include(router.urls)),
]
