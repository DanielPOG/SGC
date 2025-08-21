from rest_framework import viewsets
from .models import EstudioFormal, Complementaria #pylint:disable=relative-beyond-top-level
from .serializers import FormalSerializer, ComplementariaSerializer #pylint:disable=relative-beyond-top-level

class EstudioFormalViewSet(viewsets.ModelViewSet):
    queryset = EstudioFormal.objects.all()
    serializer_class = FormalSerializer

class EducacionComplementariaViewSet(viewsets.ModelViewSet):
    queryset = Complementaria.objects.all()
    serializer_class = ComplementariaSerializer
