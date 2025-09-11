from django.urls import path
from . import views

urlpatterns = [
    path('cargos/prueba/', views.index, name='index'),
    path('cargos/index/', views.cargoIndex, name='cargoIndex'),
    path('cargos/newcargo/', views.newcargo, name='cargo_new'),
    path('cargos/cargohistorial/', views.cargohistorial, name='cargohistorial'),
    path('cargos/nuevo_fc/', views.nuevo_fc, name='nuevo_fc'),
    path('cargos/editar_cargo/<int:id>/', views.editar_cargo, name='editar_cargo'),
    path('api/', views.api_view, name='cargos_api'),
]