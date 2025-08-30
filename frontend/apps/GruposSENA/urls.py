from django.urls import path
from . import views

urlpatterns = [
    path('grupo_sena/', views.grupo_sena, name='grupo_sena'),
    path('new_grupo/', views.new_grupo, name='new_grupo'),
    path('historial_grupo/', views.historial_grupo, name='historial_grupo'),  
]