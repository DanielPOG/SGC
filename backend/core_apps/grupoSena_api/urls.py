from django.urls import path, include
from rest_framework import routers
from . import views

# Configuración del router para ViewSets de DRF
router = routers.DefaultRouter()
router.register(r'grupo-sena', views.GrupoSenaViewSet)
router.register(r'usuario-grupo', views.UsuarioGrupoViewSet)

urlpatterns = [
    # Endpoints de APIs
    path('general/areas/', views.api_areas, name='api_areas'),
    path('usuarios/usuarios/', views.api_usuarios, name='api_usuarios'),

    # Listas basadas en clase
    path('nombre-grupo/', views.NombreGrupoList.as_view(), name='nombre-grupo-list'),
    path('estado-grupo/', views.EstadoGrupoList.as_view(), name='estado-grupo'),

    # Rutas automáticas de los ViewSets (DRF)
    path('', include(router.urls)),
]
