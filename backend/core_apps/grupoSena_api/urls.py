from django.urls import path, include
from rest_framework import routers
from . import views

# 🔹 Configuración del router para ViewSets de DRF
router = routers.DefaultRouter()
router.register(r'grupo-sena', views.GrupoSenaViewSet)
router.register(r'usuario-grupo', views.UsuarioGrupoViewSet)

urlpatterns = [
    # 🔹 Endpoints de APIs
    path('general/areas/', views.api_areas, name='api_areas'),
    # urls.py
    path('usuarios/usuarios/', views.api_usuarios, name='api_usuarios'),

    # Listas basadas en clase
    path('nombre-grupo/', views.NombreGrupoList.as_view(), name='nombre-grupo-list'),
    path('estado-grupo/', views.EstadoGrupoList.as_view(), name='estado-grupo'),

    # Endpoints para editar y actualizar desde frontend (no DRF)
    path('gruposena/editar_grupo/<int:id>/', views.editar_grupo, name='editar_grupo'),
    path('gruposena/update_grupo/<int:id>/', views.grupo_update, name='grupo_update'),

    # 🔹 Rutas automáticas de los ViewSets (DRF)
    path('', include(router.urls)),
]
