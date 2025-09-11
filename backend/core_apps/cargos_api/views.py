
from core_apps.cargos_api.services.cascada import (
    build_escalon_sugerencias,
    aplicar_decisiones_cascada,
    _normalize_date
)
from rest_framework import viewsets, status
from .models import CargoNombre, EstadoCargo, Cargo, CargoFuncion, CargoUsuario, Idp
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import pandas as pd
from core_apps.usuarios_api.models import Usuario
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.exceptions import ValidationError
import json
from .serializers import (
    CargoNombreSerializer,
    EstadoCargoSerializer,
    CargoSerializer,
    CargoFuncionSerializer,
    CargoUsuarioSerializer,
    CargoExcelSerializer,
    CargoNestedSerializer,
    CargoUsuarioNestedSerializer,
    IdpSerializer,
    IdpxCargoSerializer,
    EstadoVinculacionSerializer,
    CargoUsuarioSimpleSerializer,
    SimulacionInputSerializer,
    ConfirmacionCascadaSerializer,
    DecisionSerializer,
)

class CargoNombreViewSet(viewsets.ModelViewSet):
    queryset = CargoNombre.objects.all()
    serializer_class = CargoNombreSerializer


class EstadoCargoViewSet(viewsets.ModelViewSet):
    queryset = EstadoCargo.objects.all()
    serializer_class = EstadoCargoSerializer

class EstadoVinculacionViewSet(viewsets.ModelViewSet):
    queryset = EstadoVinculacion.objects.all()
    serializer_class = EstadoVinculacionSerializer

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
    @action(methods=['get'], detail=False)
    def historialCargos(self, request):
        idp_id = request.query_params.get('idp_id')
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
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import ValidationError


class CargoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = CargoUsuario.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "por_idp"]:
            return CargoUsuarioNestedSerializer
        return CargoUsuarioSerializer

    def perform_create(self, serializer):
        self.instance_creada = serializer.save()

    def create(self, request, *args, **kwargs):
        data = request.data.dict()  # solo campos normales
        archivo_root = request.FILES.get("resolucion_archivo")

        if "cargo" in data and "cargo_id" not in data:
            data["cargo_id"] = data.pop("cargo")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        v = serializer.validated_data

        cargo_destino_id = getattr(v.get("cargo"), "id", v.get("cargo_id")) or data.get("cargo_id")
        tipo_decision = getattr(v.get("estadoVinculacion"), "estado", "").upper()

        ocupacion_actual = CargoUsuario.objects.filter(
            cargo_id=cargo_destino_id,
            fechaRetiro__isnull=True
        ).select_related("usuario").first()

        if not ocupacion_actual:
            if archivo_root:
                serializer.validated_data["resolucion_archivo"] = archivo_root
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        usuario_id = ocupacion_actual.usuario.id
        sugerencias = build_escalon_sugerencias(usuario_id, cargo_destino_id, tipo_decision)

        if not sugerencias:
            if archivo_root:
                serializer.validated_data["resolucion_archivo"] = archivo_root
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({
            "requiere_confirmacion": True,
            "cargo_usuario": {"usuario": usuario_id},
            "sugerencias": sugerencias
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="confirmacion")
    def confirmacion(self, request, *args, **kwargs):
        data = {k: v[0] if isinstance(v, list) else v for k, v in request.data.items() if not k.startswith("decisiones[")}

        if "payload_root" in data and isinstance(data["payload_root"], str):
            try:
                data["payload_root"] = json.loads(data["payload_root"])
            except json.JSONDecodeError:
                return Response({"error": "Formato inválido en payload_root"}, status=400)

        decisiones = []
        for key in request.data:
            if key.startswith("decisiones["):
                try:
                    decisiones.append(json.loads(request.data[key]))
                except json.JSONDecodeError:
                    return Response({"error": "Formato inválido en decisiones"}, status=400)

        serializer_in = ConfirmacionCascadaSerializer(data={**data, "decisiones": decisiones})
        serializer_in.is_valid(raise_exception=True)
        validated = serializer_in.validated_data

        root_usuario_id = validated["root_usuario_id"]
        cargo_destino_id = validated.get("cargo_destino_id")
        decisiones = validated.get("decisiones", [])
        payload_root = data.get("payload_root", {})

        archivo_root = request.FILES.get("resolucion_archivo")
        if archivo_root:
            payload_root["resolucion_archivo"] = archivo_root

        if "cargo_id" not in payload_root and cargo_destino_id:
            payload_root["cargo_id"] = cargo_destino_id

        resultados = []
        archivos_a_cerrar = []

        try:
            with transaction.atomic():
                root_serializer = CargoUsuarioSerializer(
                    data=payload_root,
                    context={"cargo_destino_id": cargo_destino_id}
                )
                root_serializer.is_valid(raise_exception=True)
                root_instance = root_serializer.save()

                root_instance.usuario.cargo = root_instance.cargo
                root_instance.usuario.save(update_fields=["cargo"])

                for i, dec in enumerate(decisiones):
                    dec_payload = dec.copy()
                    archivo_dec = request.FILES.get(f"decisiones_archivo_{i}")
                    if archivo_dec:
                        dec_payload["resolucion_archivo"] = archivo_dec
                        archivos_a_cerrar.append(archivo_dec)
                    else:
                        dec_payload["resolucion_archivo"] = None

                    dec_serializer = CargoUsuarioSerializer(
                        data=dec_payload,
                        context={"cargo_destino_id": dec_payload.get("cargo_id")}
                    )
                    dec_serializer.is_valid(raise_exception=True)
                    resultados.append(dec_serializer.save())

        finally:
            if archivo_root and not archivo_root.closed:
                archivo_root.close()
            for f in archivos_a_cerrar:
                if f and not f.closed:
                    f.close()

        return Response({
            "root": CargoUsuarioSerializer(root_instance).data,
            "decisiones": CargoUsuarioSerializer(resultados, many=True).data
        }, status=status.HTTP_201_CREATED)

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
