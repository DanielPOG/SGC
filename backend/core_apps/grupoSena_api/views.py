from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import GrupoSena, NombreGrupo, EstadoGrupo, UsuarioGrupo
from .serializers import GrupoSenaSerializer, UsuarioGrupoSerializer, NombreGrupoSerializer, EstadoGrupoSerializer
from core_apps.general.models import Area
from core_apps.usuarios_api.models import Usuario
from rest_framework import status

# -------------------- DRF ViewSets --------------------
class GrupoSenaViewSet(viewsets.ModelViewSet):
    queryset = GrupoSena.objects.select_related("area", "estado", "lider", "nombre_grupo")
    serializer_class = GrupoSenaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "nombre_grupo__nombre",  
        "area__nombre",          
        "lider__nombre",         
        "lider__apellido",       
    ]
    ordering_fields = ["fecha_creacion", "fecha_fin", "capacidad"]

class UsuarioGrupoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioGrupo.objects.select_related("usuario", "grupo")
    serializer_class = UsuarioGrupoSerializer
    permission_classes = [AllowAny]

class EstadoGrupoList(APIView):
    def get(self, request):
        estados = EstadoGrupo.objects.all()
        serializer = EstadoGrupoSerializer(estados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# -------------------- APIs para selects dinámicos --------------------
def api_areas(request):
    areas = list(Area.objects.values("id", "nombre"))
    return JsonResponse(areas, safe=False)

def api_usuarios(request):
    usuarios = list(Usuario.objects.values("id", "nombre", "apellido"))
    return JsonResponse(usuarios, safe=False)

class NombreGrupoList(APIView):
    def get(self, request):
        grupos = NombreGrupo.objects.all()
        serializer = NombreGrupoSerializer(grupos, many=True)
        return Response(serializer.data)

# -------------------- Vistas para HTML --------------------
def grupo_sena(request):
    grupos = GrupoSena.objects.select_related("nombre_grupo", "area", "lider").all()
    return render(request, "layout/grupo_sena.html", {"grupos": grupos})

def new_grupo(request):
    return render(request, "pages/new_grupo.html")

def historial_grupo(request):
    return render(request, "pages/historial_grupo.html")

def editar_grupo(request, id):
    grupo = get_object_or_404(GrupoSena, id=id)
    usuarios = Usuario.objects.all()
    return render(request, "pages/editar_grupo.html", {
        "grupo": grupo,
        "usuarios": usuarios,
        "mode": "edit"
    })

@csrf_exempt
def grupo_update(request, id):
    grupo = get_object_or_404(GrupoSena, id=id)
    if request.method == "POST":
        grupo.lider_id = request.POST.get("lider") or None
        grupo.observacion = request.POST.get("observacion") or ""
        grupo.save()
        return redirect("grupo_sena")
    return redirect("editar_grupo", id=id)
