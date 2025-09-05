from django.urls import path
from . import views

urlpatterns = [
    path('solicitudes', views.solicitudes, name='solicitudes'),
   path('todas_solicitudes/', views.todas_solicitudes, name='todas_solicitudes'),
     path("solicitud/pendiente/<int:id>/", views.solicitud_pendiente, name="solicitud_pendiente"),
    path("solicitud/revicion/<int:id>/", views.solicitud_revicion, name="solicitud_revicion"),
    path("solicitud/aprovada/<int:id>/", views.solicitud_aprovada, name="solicitud_aprovada"),
    path('estado_solicitud', views.estado_solicitud, name='estado_solicitud'),
]