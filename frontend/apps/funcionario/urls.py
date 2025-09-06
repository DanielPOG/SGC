from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('cambiar_contra/', views.cambiar_contra, name='cambiar_contra'),
    path('actualizar_datos/', views.actualizar_datos, name='actualizar_datos'),
    path('agregar_formacion/', views.agregar_formacion, name='agregar_formacion'),
    path('historial_solicitudes/', views.historial_solicitudes, name='historial_solicitudes'),
]