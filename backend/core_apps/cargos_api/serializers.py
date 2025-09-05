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
    # Lógica principal (igual que antes)
    # ---------------------------
    def _post_create_update_logic(self, instance, validated_data=None):
        hoy = timezone.now()
        usuario = instance.usuario
        cargo = instance.cargo
        estado = instance.estadoVinculacion.estado.upper()

        # cerrar cargos abiertos del usuario
        abiertos = CargoUsuario.objects.filter(usuario=usuario, fechaRetiro__isnull=True).exclude(pk=instance.pk)
        for abierto in abiertos:
            abierto.fechaRetiro = hoy
            abierto.save(update_fields=["fechaRetiro"])

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

            ultimo_planta = CargoUsuario.objects.filter(
                cargo=cargo,
                estadoVinculacion__estado__iexact="PLANTA"
            ).exclude(usuario=usuario).order_by("-fechaInicio").first()
            if ultimo_planta:
                ultimo_planta.usuario.cargo = None
                ultimo_planta.usuario.save(update_fields=["cargo"])

            usuario.cargo = cargo
            usuario.save(update_fields=["cargo"])

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

        if instance.estadoVinculacion.estado.upper() == "TEMPORAL" and instance.fechaRetiro is not None:
            self._devolver_a_planta(usuario, hoy)

    # ---------------------------
    # NUEVO: construir sugerencias con opciones
    # ---------------------------
    def build_escalon_sugerencias(self, usuario, hoy=None, visited=None):
        if hoy is None:
            hoy = timezone.now()

        if visited is None:
            visited = set()

        sugerencias = []
        if usuario.pk in visited:
            return sugerencias
        visited.add(usuario.pk)

        planta_original = CargoUsuario.objects.filter(
            usuario=usuario,
            estadoVinculacion__estado__iexact="PLANTA"
        ).order_by("-fechaInicio").first()

        if not planta_original:
            return sugerencias

        opciones = []

        # opción 1 → volver a planta
        opciones.append({
            "cargo_id": planta_original.cargo.pk,
            "cargo_nombre": planta_original.cargo.cargoNombre.nombre if planta_original.cargo.cargoNombre else None,
            "tipo": "planta"
        })

        # opción 2 → cargos libres para asignar como temporal
        cargos_ocupados = CargoUsuario.objects.filter(fechaRetiro__isnull=True).values("cargo_id")
        cargos_temporales_libres = Cargo.objects.exclude(id__in=cargos_ocupados)
        for cargo in cargos_temporales_libres:
            opciones.append({
                "cargo_id": cargo.pk,
                "cargo_nombre": cargo.cargoNombre.nombre if cargo.cargoNombre else None,
                "tipo": "temporal"
            })

        # recursivo: si hay alguien ocupando el cargo de planta
        temporal_en_planta = CargoUsuario.objects.filter(
            cargo=planta_original.cargo,
            estadoVinculacion__estado__iexact="TEMPORAL",
            fechaRetiro__isnull=True
        ).first()

        if temporal_en_planta:
            # solo si hay alguien ocupando el cargo de planta → sugerencias en cascada
            sugerencias.append({
                "usuario_id": usuario.pk,
                "usuario_nombre": getattr(usuario, "nombre", str(usuario)),
                "opciones": opciones
            })
            siguiente = self.build_escalon_sugerencias(temporal_en_planta.usuario, hoy, visited=visited)
            sugerencias.extend(siguiente)

        return sugerencias


    # ---------------------------
    # devolver a planta (auto)
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
                return self.build_escalon_sugerencias(usuario, hoy, visited)

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
