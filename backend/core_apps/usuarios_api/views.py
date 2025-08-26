from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UsuarioSerializer
from .models import Usuario
# Create your views here.

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()