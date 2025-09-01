from django.urls import path
from . import views

urlpatterns = [
    path('', views.grupo_sena, name='grupo_sena'),
]
