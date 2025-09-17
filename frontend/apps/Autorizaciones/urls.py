from django.urls import path
from . import views

urlpatterns = [
    path('', views.autorizaciones, name='autorizaciones'),

    path('user_autorizado/', views.user_autorizado, name='user_autorizado'),
]
