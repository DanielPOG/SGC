from rest_framework import viewsets, status
from .models import CargoNombre, EstadoCargo, Cargo, CargoFuncion, CargoUsuario
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import pandas as pd
from core_apps.general.models import Centro

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

# VISTA PARA SUBIR POR EXCEL
class CargoUploadView(APIView):
    parser_classes = [MultiPartParser]  # Habilita la carga de archivos

    def post(self, request, format=None):
        excel_file = request.FILES.get('file')
        if not excel_file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)  # Usa openpyxl o xlrd si necesario
        except Exception as e:
            return Response({'error': f'Error reading Excel file: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        cargos_creados = []
        for index, row in df.iterrows():
            try:
                cargoNombre = CargoNombre.objects.get(nombre=row['cargoNombre'])
                estadoCargo = EstadoCargo.objects.get(estado=row['estadoCargo'])
                centro = Centro.objects.get(nombre=row['centro'])

                cargo = Cargo.objects.create(
                    cargoNombre=cargoNombre,
                    idp=row['idp'],
                    estadoCargo=estadoCargo,
                    resolucion=row['resolucion'],
                    centro=centro,
                    observacion=row.get('observacion', '')
                )
                cargos_creados.append(cargo.id)

            except Exception as e:
                return Response({'error': f'Error en fila {index + 2}: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Cargos creados correctamente', 'cargos': cargos_creados}, status=status.HTTP_201_CREATED)