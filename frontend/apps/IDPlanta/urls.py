from django.urls import path
from . import views

urlpatterns = [
    path('id_planta/', views.id_planta, name='id_planta'),

    path('newid_planta', views.newid_palnta, name='newid_planta'),
]