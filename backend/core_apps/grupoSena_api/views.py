"""
    ViewSets
"""
from rest_framework import viewsets
from .models import EstadoGrupo, GrupoSena, UsuarioGrupo
from .serializers import EstadoGrupoSerializer, GrupoSenaSerializer, UsuarioGrupoSerializer


class EstadoGrupoViewSet(viewsets.ModelViewSet):
    queryset = EstadoGrupo.objects.all()
    serializer_class = EstadoGrupoSerializer


class GrupoSenaViewSet(viewsets.ModelViewSet):
    queryset = GrupoSena.objects.all()
    serializer_class = GrupoSenaSerializer


class UsuarioGrupoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioGrupo.objects.all()
    serializer_class = UsuarioGrupoSerializer
