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
    http_method_names = ['get', 'post', 'patch']
    parser_classes = [MultiPartParser]
    def create(self, request):
        serializer = IdpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Idp.objects.filter(idp_id=request.data.get('idp_id')).exists():
            return Response({'error':'Ya existe una IDP con ese número'}, status=status.HTTP_409_CONFLICT)
        idp = serializer.save()
        return Response(IdpSerializer(idp).data, status=status.HTTP_201_CREATED)
    @action(methods=['patch'], detail=False)
    def cambiarEstado(self, request):
        idp_id = request.data.get('idp_id')
        if not idp_id:
            return Response({"error":"Error al cambiar estado"}, status=400)
        try:
            idp = Idp.objects.get(idp_id=idp_id)
        except Idp.DoesNotExist as e:
            print(f'Error al cambiar estado: {e}')
            return Response({'error':'Error al cambiar el estado de la IDP'}, status=404)
        cargo_exists = Cargo.objects.filter(idp=idp.idp_id).exists()
        if cargo_exists:
            c_obj = Cargo.objects.filter(idp=idp.idp_id).get()
            if c_obj.idp.estado is True:
                return Response({'error':'No es posible desactivar una IDP con cargos activos'}, status=400)
        idp.estado = not idp.estado
        idp.save()
        text = 'IDP Desactivado' if idp.estado is False else 'IDP Activado'
        return Response({"msg":text},status=200)

    @action(methods=['post'], detail=False)
    def cargarExcel(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No se envió ningún archivo"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            #leer el archivo y captar dataframe
            df = pd.read_excel(file)
            creados, actualizados, errores = 0,0,[]
            for i, row in df.iterrows():
                try:
                    fecha = row.get("fechaCreacion")
                    idp = row.get("idp_id")
                    estado = row.get("estado")
                    if not idp:
                        errores.append({"fila":i+2, "error":"IDP Vacío"})
                        continue
                    obj, created = Idp.objects.update_or_create(
                        idp_id=idp,
                        defaults={
                            "fechaCreacion": fecha,
                            "estado": estado
                        }
                    )
                    if created:
                        creados += 1
                    else:
                        actualizados += 1
                except Exception as e:
                    errores.append({"fila":i+2, "error":str(e)})
                return Response({
                "msg": "Archivo procesado",
                "creados": creados,
                "actualizados": actualizados,
                "errores": errores
                }, status=status.HTTP_201_CREATED)
        except Exception as e: #pylint=disable:broad-exception-caught
            return Response({"error": f"Error procesando el archivo: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)



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
