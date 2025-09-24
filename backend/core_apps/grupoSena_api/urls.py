from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'grupo-sena', views.GrupoSenaViewSet)
router.register(r'usuario-grupo', views.UsuarioGrupoViewSet)

urlpatterns = [
    path('general/areas/', views.api_areas, name='api_areas'),
    path('usuarios/usuarios/', views.api_usuarios, name='api_usuarios'),
    path('nombre-grupo/', views.NombreGrupoList.as_view(), name='nombre-grupo-list'),
    path('gruposena/editar_grupo/<int:id>/', views.editar_grupo, name='editar_grupo'),
    path('gruposena/update_grupo/<int:id>/', views.grupo_update, name='grupo_update'),

    path('', include(router.urls)),  # aquí va vacío, para que /api/gruposena/grupo-sena/ funcione
]
