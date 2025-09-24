from django.urls import path
from . import views

urlpatterns = [
    path('grupo_sena/', views.grupo_sena, name='grupo_sena'),  # Lista de grupos
    path('new_grupo/', views.new_grupo, name='new_grupo'),      # Crear nuevo grupo
    path('historial_grupo/', views.historial_grupo, name='historial_grupo'),  

    path('gruposena/editar_grupo/<int:id>/', views.editar_grupo, name='editar_grupo'),
    path('gruposena/update_grupo/<int:id>/', views.grupo_update, name='grupo_update'),
]
