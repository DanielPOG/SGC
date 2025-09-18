from django.urls import path
from . import views

urlpatterns = [
    path('id_planta/', views.id_planta, name='id_planta'),

    path('newid_planta', views.newid_palnta, name='newid_planta'),

    path('asignar_idp/', views.asignar_idp, name='asignar_idp'),
    path('editar_asig_idp/', views.editar_asig_idp, name='editar_asig_idp'),

    path('editar_idp/', views.editar_idp, name='editar_idp'),
]