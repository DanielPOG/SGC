from django.db import models
from django.utils import timezone
# Create your models here.

class CargoNombre(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre
class EstadoCargo(models.Model):
    estado = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.estado
class EstadoVinculacion(models.Model):
    estado= models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.estado
class Idp(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    fechaCreacion = models.DateField(default=timezone.now)
    def __str__(self):
        return self.numero
class Cargo(models.Model):
    cargoNombre = models.ForeignKey('CargoNombre', on_delete=models.CASCADE)
    idp = models.ForeignKey('Idp', on_delete=models.CASCADE)
    estadoCargo = models.ForeignKey('EstadoCargo', on_delete=models.CASCADE) 
    resolucion = models.CharField(max_length=200)
    resolucion_archivo = models.FileField(upload_to="resolucionesCargo/", blank=True, null=True)
    centro = models.ForeignKey('general.Centro', on_delete=models.CASCADE)
    fechaCreacion = models.DateTimeField(default=timezone.now)
    fechaActualizacion = models.DateTimeField(auto_now=True)
    observacion = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.idp)

class CargoFuncion(models.Model):
    funcion = models.TextField()
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.cargo} - {self.funcion[:30]}...'
class CargoUsuario(models.Model):
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    usuario = models.ForeignKey('usuarios_api.Usuario', on_delete=models.CASCADE)
    fechaInicio = models.DateField(auto_now_add=True)
    fechaRetiro = models.DateField(blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    grado = models.CharField(max_length=100)
    resolucion= models.CharField(max_length=100)
    resolucion_archivo = models.FileField(upload_to="resolucionesCargoUsuario/", blank=True, null=True)
    estadoVinculacion = models.ForeignKey('EstadoVinculacion', on_delete=models.CASCADE )
    def __str__(self):
        return f"{self.cargo} - {self.usuario}"
