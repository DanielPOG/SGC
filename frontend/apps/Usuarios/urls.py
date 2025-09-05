from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('principal/', views.index, name='index'),
    path('funcionario/', views.funcionario, name='funcionario'),
    path('cargo/', views.cargo, name='cargo'),
    path('grupo_sena/', views.grupo_sena, name='grupo_sena'),
    path('reportes/', views.reportes, name='reportes'),
    path('id_planta/', views.id_planta, name='id_planta'),
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('sidebar/', views.sidebar, name='sidebar'),
    path('funcionario/', views.funcionario, name='funcionario'),
    path('newfuncionario/', views.newfuncionario, name='newfuncionario'),
    path('historial_funcionario/', views.historial_funcionario, name='historial_funcionario'),
    path('datos_basicosfun/', views.datos_basicosfun, name='datos_basicosfun'),
    path('cargo_actualfun/', views.cargo_actualfun, name='cargo_actualfun'),
    path('cargos_anterioresfun/', views.cargos_anterioresfun, name='cargos_anterioresfun'),
    path('estudios_fun/', views.estudios_fun, name='estudios_fun'),
    path('editar_fun/', views.editar_fun, name='editar_fun'),
    
    

    
   
 
]
