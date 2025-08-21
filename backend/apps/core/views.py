from rest_framework import viewsets
from .serializers import EstadosSerializer, RegionalesSerializer, CentrosSerializer #pylint:disable=relative-beyond-top-level
from .models import Estados,Regionales,Centros #pylint:disable=relative-beyond-top-level
class EstadosViewSet(viewsets.ModelViewSet):
    queryset = Estados.objects.all()
    serializer_class = EstadosSerializer
class RegionalesViewSet(viewsets.ModelViewSet):
    queryset = Regionales.objects.all()
    serializer_class = RegionalesSerializer
class CentrosViewSet(viewsets.ModelViewSet):
    queryset = Centros.objects.all()
    serializer_class = CentrosSerializer
