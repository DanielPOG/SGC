from django.urls import path
from . import views

urlpatterns = [
    path('', views.cargo, name='cargo'),
    path('nuevo/', views.newcargo, name='cargo_new'),
    path('historial/', views.cargohistorial, name='cargohistorial'),
]