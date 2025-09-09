from rest_framework import viewsets, status
from .models import CargoNombre, EstadoCargo, Cargo, CargoUsuario, Idp, EstadoVinculacion
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

from .serializers import (
    CargoNombreSerializer,
    EstadoCargoSerializer,
    CargoSerializer,
    CargoUsuarioSerializer,
    CargoExcelSerializer,
    CargoNestedSerializer,
    CargoUsuarioNestedSerializer,
    IdpSerializer,
    EstadoVinculacionSerializer,
    CargoUsuarioSimpleSerializer,
    SimulacionInputSerializer,
    ConfirmacionCascadaSerializer,
)
from core_apps.cargos_api.services.cascada import (
    build_escalon_sugerencias,
    aplicar_decisiones_cascada,
    _normalize_date
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
        cargos = Cargo.objects.filter(idp__numero=numero_idp).order_by("-fechaActualizacion")
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
                    "idp": cargo.idp.numero,
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
    serializer_class = CargoUsuarioSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # 👈 aceptar JSON + archivos

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "por_idp"]:
            return CargoUsuarioNestedSerializer
        return CargoUsuarioSerializer

    def perform_create(self, serializer):
        self.instance_creada = serializer.save()

    def create(self, request, *args, **kwargs):
        self.instance_creada = None
        data = request.data.copy()

        # 🔑 Normalización: si mandan "cargo" en form-data, mapear a cargo_id
        if "cargo" in data and "cargo_id" not in data:
            data["cargo_id"] = data.pop("cargo")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        v = serializer.validated_data
        cargo_destino_id = getattr(v.get("cargo"), "id", v.get("cargo_id")) or data.get("cargo_id")
        tipo_decision = v.get("estadoVinculacion").estado.upper()

        # Verificar si el cargo destino está ocupado
        ocupacion_actual = CargoUsuario.objects.filter(
            cargo_id=cargo_destino_id,
            fechaRetiro__isnull=True
        ).select_related("usuario").first()

        if not ocupacion_actual:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        usuario_id = ocupacion_actual.usuario.id
        sugerencias = build_escalon_sugerencias(usuario_id, cargo_destino_id, tipo_decision)

        if not sugerencias:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(
            {
                "requiere_confirmacion": True,
                "cargo_usuario": {"usuario": usuario_id},
                "sugerencias": sugerencias
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="confirmacion")
    def confirmacion(self, request, *args, **kwargs):
        """
        Confirma asignaciones escalonadas:
        - payload_root → asignación principal
        - decisiones → aplicar en cascada
        """
        serializer_in = ConfirmacionCascadaSerializer(data=request.data)
        serializer_in.is_valid(raise_exception=True)
        data = serializer_in.validated_data

        root_usuario_id = data["root_usuario_id"]
        cargo_destino_id = data.get("cargo_destino_id")
        decisiones = data.get("decisiones", [])
        payload_root = serializer_in.initial_data.get("payload_root") or data.get("payload_root")
        print("Payload Root:", payload_root)

        if not payload_root:
            return Response({"error": "payload_root requerido"}, status=400)

        # Normalizar cargo_id en payload_root
        if "cargo_id" not in payload_root and "cargo" in payload_root:
            payload_root["cargo_id"] = payload_root.pop("cargo")

        # Adjuntar archivo si viene
        if "resolucion_archivo" in data and data["resolucion_archivo"]:
            payload_root["resolucion_archivo"] = data["resolucion_archivo"]

        try:
            with transaction.atomic():
                # Crear asignación raíz
                root_serializer = CargoUsuarioSerializer(
                    data=payload_root,
                    context={"cargo_destino_id": cargo_destino_id}
                )
                root_serializer.is_valid(raise_exception=True)
                root_instance = root_serializer.save()

                # Aplicar decisiones en cascada
                resultados = aplicar_decisiones_cascada(
                    root_usuario_id=root_usuario_id,
                    cargo_destino_id=cargo_destino_id,
                    decisiones=decisiones
                )

        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({
            "root": CargoUsuarioSerializer(root_instance).data,
            "decisiones": CargoUsuarioSerializer(resultados, many=True).data
        }, status=status.HTTP_201_CREATED)


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
