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
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "por_idp"]:
            return CargoUsuarioNestedSerializer
        return CargoUsuarioSerializer

    def perform_create(self, serializer):
        self.instance_creada = serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Crea un CargoUsuario:
        - Si el cargo destino está libre → crea directamente.
        - Si está ocupado → devuelve sugerencias escalonadas para confirmar.
        """
        data = request.data.copy()

        # Mapear cargo → cargo_id si viene
        if "cargo" in data and "cargo_id" not in data:
            data["cargo_id"] = data.pop("cargo")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        v = serializer.validated_data

        cargo_destino_id = getattr(v.get("cargo"), "id", v.get("cargo_id")) or data.get("cargo_id")
        tipo_decision = getattr(v.get("estadoVinculacion"), "estado", "").upper()

        # Revisar si hay ocupante activo
        ocupacion_actual = CargoUsuario.objects.filter(
            cargo_id=cargo_destino_id,
            fechaRetiro__isnull=True
        ).select_related("usuario").first()

        if not ocupacion_actual:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # Construir sugerencias si hay ocupante
        usuario_id = ocupacion_actual.usuario.id
        sugerencias = build_escalon_sugerencias(usuario_id, cargo_destino_id, tipo_decision)

        if not sugerencias:
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
        """
        Confirma asignaciones escalonadas:
        - payload_root → asignación principal
        - decisiones → aplicar en cascada
        """

        data = request.data.copy()

        # Parsear JSON si viene como string
        import json
        if "decisiones" in data and isinstance(data.get("decisiones"), str):
            try:
                data["decisiones"] = json.loads(data["decisiones"])
            except json.JSONDecodeError:
                return Response({"error": "Formato inválido en decisiones"}, status=400)

        if "payload_root" in data and isinstance(data.get("payload_root"), str):
            try:
                data["payload_root"] = json.loads(data["payload_root"])
            except json.JSONDecodeError:
                return Response({"error": "Formato inválido en payload_root"}, status=400)

        # Agrupar campos sueltos en payload_root si no viene
        if "payload_root" not in data:
            posibles_campos = [
                "cargo_id", "cargo_destino_id", "num_doc", "estadoVinculacion",
                "salario", "grado", "resolucion", "resolucion_archivo",
                "observacion", "fechaInicio", "fechaRetiro"
            ]
            payload_root = {c: data.pop(c) for c in posibles_campos if c in data}
            if payload_root:
                data["payload_root"] = payload_root

        # Validación inicial
        serializer_in = ConfirmacionCascadaSerializer(data=data)
        serializer_in.is_valid(raise_exception=True)
        validated = serializer_in.validated_data

        root_usuario_id = validated["root_usuario_id"]
        cargo_destino_id = validated.get("cargo_destino_id")
        decisiones = validated.get("decisiones", [])
        for d in decisiones:
            # asignar num_doc si solo viene usuario_id
            if "num_doc" not in d and "usuario_id" in d:
                usuario = Usuario.objects.filter(pk=d["usuario_id"]).first()
                if usuario:
                    d["num_doc"] = str(usuario.num_doc)

            # si es planta y faltan campos obligatorios, rellenar desde histórico
            if d.get("tipo") == "planta":
                usuario = Usuario.objects.get(num_doc=d["num_doc"])
                ultimo_planta = CargoUsuario.objects.filter(
                    usuario=usuario,
                    estadoVinculacion__estado__iexact="PLANTA"
                ).order_by("-fechaInicio").first()
                if ultimo_planta:
                    d.setdefault("estadoVinculacion", ultimo_planta.estadoVinculacion.id)
                    d.setdefault("salario", ultimo_planta.salario)
                    d.setdefault("grado", ultimo_planta.grado)
                    d.setdefault("resolucion", ultimo_planta.resolucion)
                    d.setdefault("fechaInicio", str(ultimo_planta.fechaInicio))


        payload_root = serializer_in.initial_data.get("payload_root", {})

        # Normalizar cargo_id en payload_root
        if "cargo_id" not in payload_root:
            if "cargo" in payload_root:
                payload_root["cargo_id"] = payload_root.pop("cargo")
            elif cargo_destino_id:
                payload_root["cargo_id"] = cargo_destino_id
            else:
                return Response({"error": {"cargo_id": ["Este campo es obligatorio"]}}, status=400)

        # Adjuntar archivo si viene
        if "resolucion_archivo" in data and data["resolucion_archivo"]:
            payload_root["resolucion_archivo"] = data["resolucion_archivo"]

        try:
            with transaction.atomic():
                # Crear asignación raíz
                payload_root["cargo_id"] = int(payload_root["cargo_id"])
                root_serializer = CargoUsuarioSerializer(
                    data=payload_root,
                    context={"cargo_destino_id": cargo_destino_id}
                )
                root_serializer.is_valid(raise_exception=True)
                root_instance = root_serializer.save()

                # Actualizar usuario con cargo
                root_instance.usuario.cargo = root_instance.cargo
                root_instance.usuario.save(update_fields=["cargo"])

                # Aplicar decisiones en cascada
                resultados = aplicar_decisiones_cascada(
                    root_usuario_id=root_usuario_id,
                    cargo_destino_id=cargo_destino_id,
                    decisiones=decisiones
                ) or []

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
