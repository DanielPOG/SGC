from rest_framework import viewsets, filters
from django.http import JsonResponse
from .models import  GrupoSena, UsuarioGrupo
from .serializers import GrupoSenaSerializer, UsuarioGrupoSerializer
from core_apps.general.models import Area
from core_apps.usuarios_api.models import Usuario

class GrupoSenaViewSet(viewsets.ModelViewSet):
    queryset = GrupoSena.objects.select_related("area", "estado", "lider")
    serializer_class = GrupoSenaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "area__nombre", "lider__nombre", "lider__apellido"]
    ordering_fields = ["fecha_creacion", "fecha_fin", "capacidad"]

class UsuarioGrupoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioGrupo.objects.select_related("usuario", "grupo")
    serializer_class = UsuarioGrupoSerializer

# APIs para selects dinámicos
def api_areas(request):
    areas = list(Area.objects.values("id", "nombre"))
    return JsonResponse(areas, safe=False)

def api_usuarios(request):
    usuarios = list(Usuario.objects.values("id", "nombre", "apellido"))
    return JsonResponse(usuarios, safe=False)
