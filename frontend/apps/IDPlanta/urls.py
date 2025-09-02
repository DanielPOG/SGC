from django.urls import path
from . import views

urlpatterns = [
    path('id_planta/', views.id_planta, name='id_planta'),
    path('crear_idp/', views.crear_idp, name='crear_idp')
]