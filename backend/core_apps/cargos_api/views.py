from rest_framework import viewsets, status
from .models import CargoNombre, EstadoCargo, Cargo, CargoFuncion, CargoUsuario, Idp
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import pandas as pd
from core_apps.usuarios_api.models import Usuario
from rest_framework.decorators import action

from .serializers import (
    CargoNombreSerializer,
    EstadoCargoSerializer,
    CargoSerializer,
    CargoFuncionSerializer,
    CargoUsuarioSerializer,
    CargoExcelSerializer,
    CargoNestedSerializer,
    CargoUsuarioNestedSerializer,
    IdpSerializer
)

class CargoNombreViewSet(viewsets.ModelViewSet):
   
    queryset = CargoNombre.objects.all()
    serializer_class = CargoNombreSerializer


class EstadoCargoViewSet(viewsets.ModelViewSet):
    
    queryset = EstadoCargo.objects.all()
    serializer_class = EstadoCargoSerializer
    
class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects.all()
    serializer_class = IdpSerializer
    def create(self, request):
        serializer = IdpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        idp = serializer.save()
        return Response(IdpSerializer(idp).data, status=status.HTTP_201_CREATED)

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    def get_serializer_class(self):
        # Usar nested solo para GET
        if self.action in ["list", "retrieve", "por_idp"]:
            return CargoNestedSerializer
        return CargoSerializer  # POST/PUT/PATCH

    def create(self, request, *args, **kwargs):
        serializer = CargoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cargo = serializer.save()
        # Devolver serializer simple para evitar errores de nested
        return Response(CargoSerializer(cargo).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="por-idp/(?P<numero_idp>[^/.]+)")
    def por_idp(self, request, numero_idp=None):
        cargos = Cargo.objects.filter(idp__idp_id=numero_idp).order_by("-fechaActualizacion")
        if not cargos.exists():
            return Response(
                {"detail": "No se encontraron cargos para este IDP"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = []
        for cargo in cargos:
            # Titular fijo (Usuario.cargo)
            titular = Usuario.objects.filter(cargo=cargo).first()

            # Encargados temporales (CargoUsuario)
            encargados = CargoUsuario.objects.filter(cargo=cargo)

            data.append({
                "cargo": {
                    "id": cargo.id,
                    "idp": cargo.idp.idp_id,
                    "nombre": cargo.cargoNombre.nombre,
                    "centro":  cargo.centro.nombre if cargo.centro else None,
                    "fechaCreacion": cargo.fechaCreacion,
                    "fechaActualizacion": cargo.fechaActualizacion,
                },
                "titular": {
                    "id": titular.id,
                    "nombre": f"{titular.nombre} {titular.apellido}",
                } if titular else None,
                "encargados": [
                    {
                        "id": cu.usuario.id,
                        "nombre": f"{cu.usuario.nombre} {cu.usuario.apellido}",
                        "estado": cu.estadoVinculacion.estado,
                        "fechaInicio": cu.fechaInicio,
                    }
                    for cu in encargados
                ],
            })

        return Response(data, status=status.HTTP_200_OK)
class CargoFuncionViewSet(viewsets.ModelViewSet):
   
    queryset = CargoFuncion.objects.all()
    serializer_class = CargoFuncionSerializer


class CargoUsuarioViewSet(viewsets.ModelViewSet):
  
    queryset = CargoUsuario.objects.all()
    serializer_class = CargoUsuarioSerializer
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "por_idp"]:
            return CargoUsuarioNestedSerializer  # para GET
        return CargoUsuarioSerializer           # para POST/PUT/PATCH/DELETE

    @action(detail=False, methods=["get"], url_path="por-idp/(?P<idp>[^/.]+)")
    def por_idp(self, request, idp=None):
        # filtrar los CargoUsuario cuyo cargo tenga ese idp
        cargos_usuario = self.get_queryset().filter(cargo__idp__idp_id=idp)
        serializer = self.get_serializer(cargos_usuario, many=True)
        return Response(serializer.data)

# VISTA PARA SUBIR POR EXCEL
class CargoUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        excel_file = request.FILES.get('file')
        if not excel_file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response({'error': f'Error leyendo Excel: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        cargos_creados = []
        for index, row in df.iterrows():
            data = {
                "cargoNombre": row['cargoNombre'],
                "idp": row['idp'],
                "estadoCargo": row['estadoCargo'],
                "resolucion": row['resolucion'],
                "centro": row['centro'],
                "observacion": row.get('observacion', ''),
                "fechaCreacion": row.get('fechaCreacion')
            }

            serializer = CargoExcelSerializer(data=data)
            if serializer.is_valid():
                cargo = serializer.save()
                cargos_creados.append(serializer.data)
            else:
                return Response({
                    'error': f'Error en fila {index + 2}',
                    'detalle': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': 'Cargos creados correctamente',
            'cargos': cargos_creados
        }, status=status.HTTP_201_CREATED)
