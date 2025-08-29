from django.urls import path
from . import views

urlpatterns = [
    path('cargos/prueba/', views.index, name='index'),
]