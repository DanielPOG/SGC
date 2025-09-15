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
import json
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
    DecisionSerializer,
)
from core_apps.cargos_api.services.cascada import (
    build_escalon_sugerencias,
    aplicar_decisiones_cascada,
    _normalize_date
)
from core_apps.cargos_api.logic.cascada_helpers import (
    devolver_a_planta,
    devolver_a_temporal,
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
        if Idp.objects.filter(numero=request.data.get('numero')).exists():
            return Response({'error':'Ya existe una IDP con ese número'}, status=status.HTTP_409_CONFLICT)
        idp = serializer.save()
        return Response(IdpSerializer(idp).data, status=status.HTTP_201_CREATED)
    @action(methods=['patch'], detail=False)
    def cambiarEstado(self, request):
        numero = request.data.get('numero')
        if not numero:
            return Response({"error":"Error al cambiar estado"}, status=400)
        try:
            idp = Idp.objects.get(numero=numero)
        except Idp.DoesNotExist as e:
            print(f'Error al cambiar estado: {e}')
            return Response({'error':'Error al cambiar el estado de la IDP'}, status=404)
        cargo_exists = Cargo.objects.filter(idp=idp.numero).exists()
        if cargo_exists:
            c_obj = Cargo.objects.filter(idp=idp.numero).get()
            if c_obj.idp.estado is True:
                return Response({'error':'No es posible desactivar una IDP con cargos activos'}, status=400)
        idp.estado = not idp.estado
        idp.save()
        text = 'IDP Desactivado' if idp.estado is False else 'IDP Activado'
        return Response({"msg":text},status=200)
    @action(detail=False, methods=["get"], url_path="historialCargos")
    def historialCargos(self, request, pk=None):
        try:
            idp = request.query_params.get('numero ')
        except Idp.DoesNotExist:
            return Response({"error": "Idp no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        # 1. Todos los cargos que han estado asociados a esta Idp
        cargos = Cargo.objects.filter(idp=idp)

        # 2. Todos los registros de usuarios que ocuparon esos cargos
        historial = CargoUsuario.objects.filter(cargo__in=cargos).order_by("fechaInicio")

        # 3. Serializar el historial
        serializer = CargoUsuarioSerializer(historial, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
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
                    idp = row.get("numero")
                    estado = row.get("estado")
                    if not idp:
                        errores.append({"fila":i+2, "error":"IDP Vacío"})
                        continue
                    obj, created = Idp.objects.update_or_create(
                        numero=idp,
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
        data = request.data.dict()
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
        """
        Endpoint para confirmar la asignación en cascada:
        - root_usuario_id -> ID del usuario principal
        - cargo_destino_id -> ID del cargo destino
        - payload_root -> datos del usuario principal (JSON)
        - decisiones[i] -> lista de decisiones adicionales (JSON)
        - resolucion_archivo -> archivo principal
        - decisiones_archivo_i -> archivos asociados a decisiones
        """
        # --- Normalizar datos base ---
        data = {k: v[0] if isinstance(v, list) else v
                for k, v in request.data.items()
                if not k.startswith("decisiones[")}

        if "payload_root" in data and isinstance(data["payload_root"], str):
            try:
                data["payload_root"] = json.loads(data["payload_root"])
            except json.JSONDecodeError:
                return Response({"error": "Formato inválido en payload_root"}, status=400)

        payload_root = data.get("payload_root", {})
        root_usuario_id = data.get("root_usuario_id")
        cargo_destino_id = data.get("cargo_destino_id")

        # --- Parsear decisiones ---
        decisiones = []
        for key, value in request.data.items():
            if key.startswith("decisiones["):
                try:
                    decisiones.append(json.loads(value))
                except json.JSONDecodeError:
                    return Response({"error": f"Formato inválido en {key}"}, status=400)

        # Incluir archivo principal si lo hay
        archivo_root = request.FILES.get("resolucion_archivo")
        if archivo_root:
            payload_root["resolucion_archivo"] = archivo_root

        if "cargo_id" not in payload_root and cargo_destino_id:
            payload_root["cargo_id"] = cargo_destino_id

        resultados = []
        root_instance = None

        try:
            with transaction.atomic():
                # --- Procesar root ---
                root_serializer = CargoUsuarioSerializer(
                    data=payload_root,
                    context={"cargo_destino_id": cargo_destino_id}
                )
                root_serializer.is_valid(raise_exception=True)
                root_instance = root_serializer.save()

                if hasattr(root_instance, "usuario") and \
                    root_instance.estadoVinculacion.estado.upper() == "PLANTA":
                        root_instance.usuario.cargo = root_instance.cargo
                        root_instance.usuario.save(update_fields=["cargo"])

                # --- Procesar decisiones ---
                for i, dec in enumerate(decisiones):
                    usuario_id = dec.get("usuario_id")
                    tipo = dec.get("tipo", "").upper()
                    cargo_id = dec.get("cargo_id")

                    try:
                        usuario = Usuario.objects.get(pk=usuario_id)
                    except Usuario.DoesNotExist:
                        return Response({"error": f"Usuario {usuario_id} no encontrado"}, status=400)

                    if tipo == "PLANTA":
                        nuevo = devolver_a_planta(usuario, context={"request": request})
                        if nuevo:
                            resultados.append(nuevo)

                    elif tipo == "TEMPORAL":
                        archivo_dec = request.FILES.get(f"decisiones_archivo_{i}")
                        if not cargo_id:
                            return Response({"error": f"Falta cargo_id en decisión {i}"}, status=400)
                        try:
                            cargo_destino = Cargo.objects.get(pk=cargo_id)
                        except Cargo.DoesNotExist:
                            return Response({"error": f"Cargo {cargo_id} no encontrado"}, status=400)

                        nuevo = devolver_a_temporal(
                            usuario=usuario,
                            cargo_destino=cargo_destino,
                            datos_temporal=dec,
                            resolucion_archivo=archivo_dec,
                            context={"request": request}
                        )
                        resultados.append(nuevo)


                    else:
                        return Response({"error": f"Tipo de decisión inválido: {tipo}"}, status=400)

        finally:
            if archivo_root and not archivo_root.closed:
                archivo_root.close()
            for f in request.FILES.values():
                if f and not f.closed:
                    f.close()

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
