from rest_framework import viewsets
from models import NombresCargo, Cargos, UsuariosCargo
from serializers import NombresSerializer, CargosSerializer, UsuariosCargoSerializer

class CargosViewSet(viewsets.ModelViewSet):
    queryset = Cargos.objects.all()
    serializer_class = CargosSerializer

class NombresViewSet(viewsets.ModelViewSet):
    queryset = NombresCargo.objects.all()
    serializer_class = NombresSerializer

class UsuarioCargoViewSet(viewsets.ModelViewSet):
    queryset = UsuariosCargo.objects.all()
    serializer_class = UsuariosCargoSerializer