from django.db import models
from core_apps.general.models import Area
from django.apps import apps

# Create your models here.

class CargoNombre(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

class EstadoCargo(models.Model):
    estado = models.CharField(max_length=100, unique=True)
class Cargo(models.Model):
    codigoCargo = models.CharField(max_length=10, unique=True)
    cargoNombre = models.ForeignKey('CargoNombre', on_delete=models.CASCADE)
    idp = models.CharField(max_length=10)
    estadoCargo = models.ForeignKey('EstadoCargo', on_delete=models.CASCADE) 
    resolucion = models.CharField(max_length=200)
    centro = models.ForeignKey('general.Centro', on_delete=models.CASCADE)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaActualizacion = models.DateTimeField(auto_now=True)
    observacion = models.TextField(blank=True, null=True)
class CargoFuncion(models.Model):
    funcion = models.TextField()
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE)

class CargoUsuario(models.Model):
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    usuario = models.ForeignKey('usuarios_api.Usuario', on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaRetiro = models.DateTimeField(auto_now=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    grado = models.CharField(max_length=100)
    resolucion= models.CharField(max_length=100)