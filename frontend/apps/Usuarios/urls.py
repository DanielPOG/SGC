from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('', views.index, name='index'),
    path('pr', views.pr, name='pr'),
    path('funcionario/', views.funcionario, name='funcionario'),
    path('cargo/', views.cargo, name='cargo'),
    path('grupo_sena/', views.grupo_sena, name='grupo_sena'),
    path('reportes/', views.reportes, name='reportes'),
    path('id_planta/', views.id_planta, name='id_planta'),
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('sidebar/', views.sidebar, name='sidebar'),
]
