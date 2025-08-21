from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.apps import apps
# Create your models here.
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)
class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10)
class EstudioFormal(models.Model):
    nombre = models.CharField(max_length=50)
# Gestor de usuarios personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, apellido, password=None):
        if not correo:
            raise ValueError('El correo es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, nombre=nombre, apellido=apellido)
        user.set_password(password)  # Cifra la contraseña
        user.save(using=self._db)
        return user
    
    def create_superuser(self, correo, nombre, apellido, password=None):
        user = self.create_user(correo, nombre, apellido, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Modelo de Usuario personalizado
def get_cargo_model():
    return apps.get_model('cargos_api', 'Cargo')

# Modelo de Usuario personalizado
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    num_doc = models.CharField(max_length=20)
    tipo_doc = models.ForeignKey('TipoDocumento', on_delete=models.CASCADE)
    correo = models.EmailField(max_length=254, unique=True)
    genero = models.ForeignKey('Genero', on_delete=models.CASCADE)

    # Usar la función get_cargo_model() para evitar el ciclo de importación circular
    cargo = models.ForeignKey(get_cargo_model(), on_delete=models.CASCADE) 
    
    estudioF = models.ForeignKey('EstudioFormal', on_delete=models.CASCADE)
    
    # Campos adicionales necesarios para la autenticación
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    
    # Establecer el nombre del campo de usuario (el correo será el principal)
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'num_doc']

    objects = UsuarioManager() 

    def __str__(self):
        return self.correo

    # Métodos necesarios para el sistema de autenticación y permisos
    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff

class FormacionComplementaria(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    certificado = models.FileField(upload_to='certificados/')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Bitacora(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255) #TODO : MANEJAR EN LOGICA PARA AGREGAR A BITACORA
    fecha = models.DateTimeField(auto_now_add=True)