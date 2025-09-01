from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),  # página raíz = login
    path('principal/', views.index, name='index'), # index con sidebar
    path('funcionario/', views.funcionario, name='funcionario'),
]
