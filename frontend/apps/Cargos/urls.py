from django.urls import path
from . import views

urlpatterns = [
    path('cargos/prueba/', views.index, name='index'),
    path('cargoos/newcargo/', views.newcargo, name='cargo_new'),
    path('cargos/cargohistorial/', views.cargohistorial, name='cargohistorial'),
    path('cargos/nuevo_fc/', views.nuevo_fc, name='nuevo_fc'),
]