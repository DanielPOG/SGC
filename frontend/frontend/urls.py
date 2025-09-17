"""
URL configuration for frontend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('', include('apps.Usuarios.urls')),  #Ruta raíz que carga login_view

    path('admin/', admin.site.urls),
    path('usuarios/', include('apps.Usuarios.urls')), # URLS de la app Usuarios 
    path('cargos/', include('apps.Cargos.urls')), # URLS de la app Cargos
    path('gruposena/', include('apps.GruposSENA.urls')), # URLS de la app GruposSENA
    path('reportes/', include('apps.Reportes.urls')), # URLS de la app Reportes
    path('idplanta/', include('apps.IDPlanta.urls')), # URLS de la app IDPlanta
    path('solicitudes/', include('apps.Solicitudes.urls')), # URLS de la app Solicitudes
    path('autorizaciones/', include('apps.Autorizaciones.urls')), # URLS de la app Autorizaciones
    path('bitacora/', include('apps.Bitacora.urls')), # URLS de la app Bitacora
    path('funcionario/', include('apps.funcionario.urls')), # URLS de la app funcionario
]
