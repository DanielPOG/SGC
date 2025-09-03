from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('cambiar_contra/', views.cambiar_contra, name='cambiar_contra'),

]