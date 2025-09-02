from django.urls import path
from . import views

urlpatterns = [
    path('solicitudes', views.solicitudes, name='solicitudes'),
    path('todas_solicitudes', views.todas_solicitudes, name='todas_solicitudes'),
    path('solicitud_pendiente', views.solicitud_pendiente, name='solicitud_pendiente'), 
    path('solicitud_revicion', views.solicitud_revicion, name='solicitud_revicion'),
    
 
]