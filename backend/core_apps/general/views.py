from rest_framework import viewsets
from .serializers import (
    RegionalSerializer, 
    CentroSerializer, 
    RedSerializer, 
    AreaSerializer, 
    DependenciaSerializer
)
from .models import Regional, Centro, Red, Area, Dependencia


class RegionalViewSet(viewsets.ModelViewSet):
    queryset = Regional.objects.all()
    serializer_class = RegionalSerializer


class CentroViewSet(viewsets.ModelViewSet):
    queryset = Centro.objects.all()
    serializer_class = CentroSerializer


class RedViewSet(viewsets.ModelViewSet):
    queryset = Red.objects.all()
    serializer_class = RedSerializer


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class DependenciaViewSet(viewsets.ModelViewSet):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer

