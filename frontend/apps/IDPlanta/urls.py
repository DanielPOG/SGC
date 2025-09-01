from django.urls import path
from . import views

urlpatterns = [
    path('', views.id_planta, name='id_planta'),
]
