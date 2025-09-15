from django.db import models
from django.utils import timezone
from datetime import datetime
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
    idp_id = models.CharField(max_length=10,unique=True, primary_key=True, default='0')
    fechaCreacion = models.DateField(default=timezone.now)
    estado  = models.BooleanField(default=True)
    def __str__(self):
        return self.idp_id
class Cargo(models.Model):
    cargoNombre = models.ForeignKey('CargoNombre', on_delete=models.CASCADE)
    idp = models.ForeignKey('Idp', on_delete=models.CASCADE)
    estadoCargo = models.ForeignKey('EstadoCargo', on_delete=models.CASCADE)
    resolucion = models.CharField(max_length=200)
    resolucion_archivo = models.FileField(upload_to="resolucionesCargo/", blank=True, null=True)
    centro = models.ForeignKey('general.Centro', on_delete=models.CASCADE)
    fechaCreacion = models.DateTimeField(default=timezone.now)
    fechaActualizacion = models.DateTimeField(auto_now=True, null=True, blank=True)
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

class IdpxCargo(models.Model):
    idp = models.ForeignKey(
    "Idp",
    null=True,
    on_delete=models.CASCADE,
    related_name="historial_cargos",
    )
    cargo = models.ForeignKey(
        "Cargo",
        on_delete=models.CASCADE,
        related_name="historial_idps"
    )
    fecha_asignacion = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)







