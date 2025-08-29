from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.apps import apps
from datetime import date
from core_apps.cargos_api.models import Cargo
from core_apps.general.models import Dependencia

from django.contrib.contenttypes.models import ContentType #PARA BITACORA
from django.contrib.contenttypes.fields import GenericForeignKey #PARA BITACORA
# Create your models here.
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    sigla = models.CharField(max_length=10, unique=True)
    def __str__(self): return self.nombre
class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    sigla = models.CharField(max_length=10, unique=True)
    def __str__(self): return self.nombre
class EstudioFormal(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.nombre
# Gestor de usuarios personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, apellido, num_doc, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es obligatorio')
        if password is None:
            raise ValueError('La contraseña es obligatoria')  # opcional pero recomendado

        correo = self.normalize_email(correo)
        user = self.model(
            correo=correo,
            nombre=nombre,
            apellido=apellido,
            num_doc=num_doc,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre, apellido, num_doc, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_staff=True e is_superuser=True')

        tipo_doc, _ = TipoDocumento.objects.get_or_create(sigla='CC', defaults={'nombre': 'Cédula'})
        genero, _ = Genero.objects.get_or_create(sigla='ND', defaults={'nombre': 'No definido'})
        estudio, _ = EstudioFormal.objects.get_or_create(nombre='No aplica')
        rol, _ = Rol.objects.get_or_create(nombre='Admin')
        estado, _ = Estado.objects.get_or_create(nombre='Activo')
        dep, _ = Dependencia.objects.get_or_create(codigoDependencia='000', defaults={'nombre': 'General'})
        cargo, _ = Cargo.objects.get_or_create(idp='ADM-000', defaults={
            'cargoNombre': CargoNombre.objects.first(),  # ajusta a tu semilla
            'estadoCargo': EstadoCargo.objects.first(),
            'resolucion': 'N/A',
            'centro': Centro.objects.first(),
        })

        extra_fields.setdefault('tipo_doc', tipo_doc)
        extra_fields.setdefault('genero', genero)
        extra_fields.setdefault('cargo', cargo)
        extra_fields.setdefault('estudioF', estudio)
        extra_fields.setdefault('rol', rol)
        extra_fields.setdefault('fecha_n', date.today())
        extra_fields.setdefault('resolucion', "0")
        extra_fields.setdefault('estado', estado)
        extra_fields.setdefault('dependencia', dep)
        extra_fields.setdefault('software', 1)

        return self.create_user(correo, nombre, apellido, num_doc, password, **extra_fields)

# Modelo de Usuario personalizado
from django.db.models import UniqueConstraint, PROTECT

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    num_doc = models.CharField(max_length=20, db_index=True)
    tipo_doc = models.ForeignKey('TipoDocumento', on_delete=PROTECT)
    correo = models.EmailField(max_length=254, unique=True)
    genero = models.ForeignKey('Genero', on_delete=PROTECT)
    cargo = models.ForeignKey('cargos_api.Cargo', on_delete=PROTECT)
    estudioF = models.ForeignKey('EstudioFormal', on_delete=PROTECT)
    fechaInicio = models.DateField(auto_now_add=True)
    fechaActualizacion = models.DateField(auto_now=True, null=True, blank=True)
    fechaRetiro = models.DateField(null=True, blank=True)
    rol = models.ForeignKey('Rol', on_delete=PROTECT)
    fecha_n = models.DateField()
    resolucion = models.CharField(max_length=100)
    estado = models.ForeignKey('Estado', on_delete=PROTECT)
    dependencia = models.ForeignKey('general.Dependencia', on_delete=PROTECT)

    SOFTWARE_OPCIONES = (
        (0, "Sin acceso"),
        (1, "Acceso básico"),
        (2, "Acceso avanzado"),
    )
    software = models.PositiveSmallIntegerField(choices=SOFTWARE_OPCIONES, default=1)

    # Auth
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_superuser lo hereda de PermissionsMixin
    # last_login lo hereda de AbstractBaseUser (déjalo tal cual, no lo redefinas)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'num_doc']

    objects = UsuarioManager()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['tipo_doc', 'num_doc'], name='uniq_tipo_doc_num_doc')
        ]

    def __str__(self):
        return self.correo

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}".strip()

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff

def certificado_upload_to(instance, filename):
    return f'certificados/{instance.usuario_id}/{filename}'

class TipoCertificado(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nombre

class FormacionComplementaria(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey('TipoCertificado', on_delete=PROTECT)
    institucion = models.CharField(max_length=100)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    certificado = models.FileField(upload_to=certificado_upload_to)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.fechaFin < self.fechaInicio:
            raise ValidationError("fechaFin no puede ser anterior a fechaInicio")

    def __str__(self):
        return f"{self.nombre} - {self.usuario.correo}" 
class Accion(models.TextChoices):
    CREAR = "CREAR", "Crear"
    ACTUALIZAR = "ACTUALIZAR", "Actualizar"
    ELIMINAR = "ELIMINAR", "Eliminar"
    LOGIN = "LOGIN", "Inicio de sesión"
    LOGOUT = "LOGOUT", "Cierre de sesión"

class Bitacora(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=20, choices=Accion.choices)
    fecha = models.DateTimeField(auto_now_add=True)

    # Objeto sobre el que se actuó
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=50, null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Contexto extra
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    cambios = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha']
class EstadoSolicitud(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nombre

class TipoSolicitud(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nombre

class Solicitud(models.Model):
    emisor = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    receptor = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='solicitudes_recibidas')
    descripcion = models.TextField()
    tipo = models.ForeignKey('TipoSolicitud', on_delete=PROTECT)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaAprobada = models.DateTimeField(null=True, blank=True)  
    estado = models.ForeignKey('EstadoSolicitud', on_delete=PROTECT)