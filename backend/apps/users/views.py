from rest_framework import viewsets
from .models import Usuarios, Generos, TiposDoc #pylint: disable=relative-beyond-top-level
from .serializers import UsuarioSerializer, GeneroSerializer, TipoDocSerializer #pylint: disable=relative-beyond-top-level
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuarioSerializer
class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Generos.objects.all()
    serializer_class = GeneroSerializer
class TipoDocViewSet(viewsets.ModelViewSet):
    queryset = TiposDoc.objects.all()
    serializer_class = TipoDocSerializer
