from rest_framework import viewsets
from .serializers import UsuarioSerializer, FormacionComplementariaSerializer
from .models import Usuario, FormacionComplementaria
# Create your views here.

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

class FComplementariaViewSet(viewsets.ModelViewSet):
    serializer_class = FormacionComplementariaSerializer
    querset=FormacionComplementaria