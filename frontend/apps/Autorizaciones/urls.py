from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.autorizaciones, name='autorizaciones'),
]