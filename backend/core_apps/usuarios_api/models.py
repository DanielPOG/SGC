from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.apps import apps
# Create your models here.
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)
    def __str__(self): #pylint:disable=invalid-str-returned
        return self.nombre
class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10)
    def __str__(self): #pylint:disable=invalid-str-returned
        return self.nombre
class EstudioFormal(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self): #pylint:disable=invalid-str-returned
        return self.nombre
class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self): #pylint:disable=invalid-str-returned
        return self.nombre
class Estado(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self): #pylint:disable=invalid-str-returned
        return self.nombre
# Gestor de usuarios personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, apellido, num_doc, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es obligatorio')
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

        return self.create_user(
            correo=correo,
            nombre=nombre,
            apellido=apellido,
            num_doc=num_doc,
            password=password,
            **extra_fields
        )


# Modelo de Usuario personalizado
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    num_doc = models.CharField(max_length=20)
    tipo_doc = models.ForeignKey('TipoDocumento', on_delete=models.CASCADE, null=True, blank=True)
    correo = models.EmailField(max_length=254, unique=True)
    genero = models.ForeignKey('Genero', on_delete=models.CASCADE, null=True, blank=True)
    cargo = models.ForeignKey('cargos_api.Cargo', on_delete=models.CASCADE,null=True, blank=True)
    estudioF = models.ForeignKey('EstudioFormal', on_delete=models.CASCADE,null=True, blank=True)
    fechaInicio = models.DateField(auto_now_add=True)
    fechaActualizacion = models.DateField(auto_now=True)
    fechaRetiro=models.DateField(null=True, blank=True)
    rol = models.ForeignKey('Rol', on_delete=models.CASCADE)
    fecha_n= models.DateField()
    resolucion= models.CharField(max_length=100)
    estado= models.ForeignKey('Estado', on_delete=models.CASCADE)
    dependencia = models.ForeignKey('general.Dependencia', on_delete=models.CASCADE)
    software= models.IntegerField()

    # Campos de autenticación
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'num_doc']

    objects = UsuarioManager()

    def __str__(self): #pylint:disable=invalid-str-returned
        return self.correo

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff

class TipoCertificado(models.Model):
    nombre= models.CharField(max_length=100)
    def __str__(self): #pylint:disable=invalid-str-returned
        return self.nombre 
class FormacionComplementaria(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey('TipoCertificado', on_delete=models.CASCADE)
    institucion = models.CharField(max_length=100)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    certificado = models.FileField(upload_to='certificados/')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Bitacora(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255) #  MANEJAR EN LOGICA PARA AGREGAR A BITACORA
    fecha = models.DateTimeField(auto_now_add=True)

class EstadoSolicitud(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): #pylint:disable=invalid-str-returned
        return self.nombre
class TipoSolicitud(models.Model):
    nombre= models.CharField(max_length=100)
    def __str__(self): #pylint:disable=invalid-str-returned
        return self.nombre
    
class Solicitud(models.Model):
    emisor = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    receptor = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='solicitudes_recibidas')
    descripcion = models.TextField()
    tipo = models.ForeignKey('TipoSolicitud', on_delete=models.CASCADE)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaAprovada = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey('EstadoSolicitud', on_delete=models.CASCADE)