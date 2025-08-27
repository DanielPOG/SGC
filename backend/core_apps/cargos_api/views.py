from rest_framework import viewsets
from .models import CargoNombre, EstadoCargo, Cargo, CargoFuncion, CargoUsuario
from .serializers import (
    CargoNombreSerializer,
    EstadoCargoSerializer,
    CargoSerializer,
    CargoFuncionSerializer,
    CargoUsuarioSerializer
)


class CargoNombreViewSet(viewsets.ModelViewSet):
   
    queryset = CargoNombre.objects.all()
    serializer_class = CargoNombreSerializer


class EstadoCargoViewSet(viewsets.ModelViewSet):
    
    queryset = EstadoCargo.objects.all()
    serializer_class = EstadoCargoSerializer


class CargoViewSet(viewsets.ModelViewSet):
   
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class CargoFuncionViewSet(viewsets.ModelViewSet):
   
    queryset = CargoFuncion.objects.all()
    serializer_class = CargoFuncionSerializer


class CargoUsuarioViewSet(viewsets.ModelViewSet):
  
    queryset = CargoUsuario.objects.all()
    serializer_class = CargoUsuarioSerializer
