from django.urls import path
from . import views

urlpatterns = [
    path('solicitudes', views.solicitudes, name='solicitudes'),
    path('todas_solicitudes', views.todas_solicitudes, name='todas_solicitudes'),
 
]