from django.urls import path
from . import views

urlpatterns = [
    path('grupo_sena/', views.grupo_sena, name='grupo_sena'),
]