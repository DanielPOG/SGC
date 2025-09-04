"""
    Serializadores de los modelos app cargos_api
"""
from rest_framework import serializers
from core_apps.general.models import Centro
from core_apps.usuarios_api.models import Usuario
from core_apps.usuarios_api.serializers import UsuarioSerializer
from .models import CargoNombre, EstadoCargo, Cargo, CargoUsuario, Idp, EstadoVinculacion
from core_apps.general.views import CentroSerializer
from django.utils import timezone
class CargoNombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoNombre
        fields = '__all__'


class EstadoCargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCargo
        fields = '__all__'
class EstadoVinculacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoVinculacion
        fields = '__all__'
        
class IdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idp
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    cargoNombre = serializers.PrimaryKeyRelatedField(queryset= CargoNombre.objects.all())
    estadoCargo = serializers.PrimaryKeyRelatedField(queryset= EstadoCargo.objects.all())
    centro = serializers.PrimaryKeyRelatedField(queryset= Centro.objects.all())
    idp = serializers.PrimaryKeyRelatedField(queryset= Idp.objects.all())
    fechaActualizacion = serializers.DateTimeField(read_only=True) 
    class Meta:
        model = Cargo
        fields = '__all__'

class CargoUsuarioSerializer(serializers.ModelSerializer):
    num_doc = serializers.CharField(write_only=True)

    class Meta:
        model = CargoUsuario
        fields = [
            "id", "cargo", "usuario", "num_doc",
            "estadoVinculacion", "salario", "grado",
            "resolucion", "resolucion_archivo",
            "observacion", "fechaInicio", "fechaRetiro"
        ]
        extra_kwargs = {"usuario": {"read_only": True}}

    # ---------------------------
    # create / update
    # ---------------------------
    def create(self, validated_data):
        num_doc = validated_data.pop("num_doc")
        try:
            usuario = Usuario.objects.get(num_doc=num_doc)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"usuario": "No existe un usuario con ese documento"})

        validated_data["usuario"] = usuario
        validated_data["fechaInicio"] = timezone.now()

        # Validación: no permitir TEMPORAL si ya hay PLANTA activo en ese cargo
        if validated_data["estadoVinculacion"].estado.upper() == "TEMPORAL":
            activo_planta = CargoUsuario.objects.filter(
                cargo=validated_data["cargo"],
                estadoVinculacion__estado__iexact="PLANTA",
                fechaRetiro__isnull=True
            ).first()
            if activo_planta:
                raise serializers.ValidationError(
                    {"cargo": f"No se puede asignar temporal. El cargo PLANTA ya está siendo cursado por {activo_planta.usuario.nombre}"}
                )

        instance = super().create(validated_data)
        self._post_create_update_logic(instance)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self._post_create_update_logic(instance, validated_data=validated_data)
        return instance

    # ---------------------------
    # Lógica principal
    # ---------------------------
    def _post_create_update_logic(self, instance, validated_data=None):
        hoy = timezone.now()
        usuario = instance.usuario
        cargo = instance.cargo
        estado = instance.estadoVinculacion.estado.upper()

        # 1) Cerrar otros cargos activos del mismo usuario
        abiertos = CargoUsuario.objects.filter(usuario=usuario, fechaRetiro__isnull=True).exclude(pk=instance.pk)
        for abierto in abiertos:
            abierto.fechaRetiro = hoy
            abierto.save(update_fields=["fechaRetiro"])

        # 2) Si el registro actual es PLANTA
        if estado == "PLANTA":
            titulares = CargoUsuario.objects.filter(cargo=cargo, fechaRetiro__isnull=True).exclude(pk=instance.pk)
            for titular in titulares:
                titular.fechaRetiro = hoy
                titular.save(update_fields=["fechaRetiro"])

                if titular.estadoVinculacion.estado.upper() == "PLANTA":
                    titular.usuario.cargo = None
                    titular.usuario.save(update_fields=["cargo"])
                elif titular.estadoVinculacion.estado.upper() == "TEMPORAL":
                    self._devolver_a_planta(titular.usuario, hoy)

            # ⚡️ FIX NUEVO:
            # Si alguien tenía este cargo en PLANTA (aunque ya cerrado), aseguramos que quede sin cargo fijo
            ultimo_planta = CargoUsuario.objects.filter(
                cargo=cargo,
                estadoVinculacion__estado__iexact="PLANTA"
            ).exclude(usuario=usuario).order_by("-fechaInicio").first()
            if ultimo_planta:
                ultimo_planta.usuario.cargo = None
                ultimo_planta.usuario.save(update_fields=["cargo"])

            # Asignamos el cargo fijo al usuario actual
            usuario.cargo = cargo
            usuario.save(update_fields=["cargo"])

        # 3) Si el registro actual es TEMPORAL
        elif estado == "TEMPORAL":
            planta_activa = CargoUsuario.objects.filter(
                usuario=usuario,
                estadoVinculacion__estado__iexact="PLANTA",
                fechaRetiro__isnull=True
            ).exclude(pk=instance.pk)
            for p in planta_activa:
                p.fechaRetiro = hoy
                p.save(update_fields=["fechaRetiro"])
                p.usuario.cargo = None
                p.usuario.save(update_fields=["cargo"])

        # 4) Si cerraron un TEMPORAL, devolver en cascada
        if instance.estadoVinculacion.estado.upper() == "TEMPORAL" and instance.fechaRetiro is not None:
            self._devolver_a_planta(usuario, hoy)

    # ---------------------------
    # Retornar a planta en cascada
    # ---------------------------
    def _devolver_a_planta(self, usuario, hoy, visited=None, modo="auto"):
        if visited is None:
            visited = set()
        if usuario.pk in visited:
            return
        visited.add(usuario.pk)

        planta_original = CargoUsuario.objects.filter(
            usuario=usuario,
            estadoVinculacion__estado__iexact="PLANTA"
        ).order_by("-fechaInicio").first()

        if planta_original:
            if modo == "escalonado":
                # 🚨 En este caso NO reasignamos aún, devolvemos sugerencia
                return {
                    "usuario": usuario.id,
                    "usuario_nombre": usuario.nombre,
                    "cargo_sugerido": planta_original.cargo.id,
                    "cargo_nombre": planta_original.cargo.cargoNombre.nombre,
                }

            # ✅ modo automático → como lo tienes ahora
            nuevo = CargoUsuario.objects.create(
                usuario=usuario,
                cargo=planta_original.cargo,
                estadoVinculacion=planta_original.estadoVinculacion,
                salario=planta_original.salario,
                grado=planta_original.grado,
                resolucion=planta_original.resolucion,
                resolucion_archivo=planta_original.resolucion_archivo,
                observacion="Retorno automático a su cargo de planta",
                fechaInicio=hoy
            )
            usuario.cargo = planta_original.cargo
            usuario.save(update_fields=["cargo"])

            temporal_en_planta = CargoUsuario.objects.filter(
                cargo=planta_original.cargo,
                estadoVinculacion__estado__iexact="TEMPORAL",
                fechaRetiro__isnull=True
            ).first()
            if temporal_en_planta:
                temporal_en_planta.fechaRetiro = hoy
                temporal_en_planta.save(update_fields=["fechaRetiro"])
                self._devolver_a_planta(temporal_en_planta.usuario, hoy, visited=visited, modo=modo)
        else:
            usuario.cargo = None
            usuario.save(update_fields=["cargo"])


class CargoExcelSerializer(serializers.ModelSerializer):
    cargoNombre = serializers.SlugRelatedField(
        queryset=CargoNombre.objects.all(),
        slug_field="nombre"
    )
    estadoCargo = serializers.SlugRelatedField(
        queryset=EstadoCargo.objects.all(),
        slug_field="estado"
    )
    centro = serializers.SlugRelatedField(
        queryset=Centro.objects.all(),
        slug_field="nombre"
    )
    idp = serializers.SlugRelatedField(
        queryset=Idp.objects.all(),
        slug_field="numero"
    )

    class Meta:
        model = Cargo
        fields = '__all__'


# Serializer anidado (para lectura: GET list y retrieve)
class CargoNestedSerializer(serializers.ModelSerializer): #sirve para mostrar los detalles del cargo
    cargoNombre = CargoNombreSerializer(read_only=True)
    estadoCargo = EstadoCargoSerializer(read_only=True)
    centro = CentroSerializer(read_only=True)
    idp = IdpSerializer(read_only=True)
    fechaCreacion = serializers.DateTimeField(read_only=True)
    fechaActualizacion = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Cargo
        fields = "__all__"

class CargoUsuarioNestedSerializer(serializers.ModelSerializer):
    cargo = CargoNestedSerializer(read_only=True)  
    usuario = UsuarioSerializer(read_only=True)    
    estado = EstadoCargoSerializer(read_only=True)
    class Meta:
        model = CargoUsuario
        fields = '__all__'
