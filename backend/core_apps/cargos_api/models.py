from django.db import models
from core_apps.general.models import Area, Regional
from django.apps import apps
from django.utils import timezone
# Create your models here.

class CargoNombre(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    funcion = models.TextField(default="Sin función registrada")
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
    fechaCreacion = models.DateField(default=timezone.now,)
    estado = models.BooleanField(default=False)
    def __str__(self):
        return self.numero
class Cargo(models.Model):
    cargoNombre = models.ForeignKey('CargoNombre', on_delete=models.CASCADE)
    idp = models.ForeignKey('Idp', on_delete=models.CASCADE, blank=True, null=True)
    estadoCargo = models.ForeignKey('EstadoCargo', on_delete=models.CASCADE) 
    resolucion = models.CharField(max_length=200, null=True, blank=True)
    resolucion_archivo = models.FileField(upload_to="resolucionesCargo/", blank=True, null=True)
    centro = models.ForeignKey('general.Centro', on_delete=models.CASCADE, blank=True, null=True)
    fechaCreacion = models.DateTimeField(default=timezone.now,null=True, blank=True)
    fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    regional = models.ForeignKey(Regional, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.idp)


class CargoUsuario(models.Model):
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    usuario = models.ForeignKey('usuarios_api.Usuario', on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField(default=timezone.now)
    fechaRetiro = models.DateTimeField(blank=True, null=True)

    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    grado = models.CharField(max_length=100,  null=True)
    resolucion= models.CharField(max_length=100,  null=True)
    resolucion_archivo = models.FileField(upload_to="resolucionesCargoUsuario/", blank=True, null=True)
    estadoVinculacion = models.ForeignKey('EstadoVinculacion', on_delete=models.CASCADE )
    observacion = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.cargo} - {self.usuario}"
    
class RelacionCascada(models.Model):
    cargo_padre = models.ForeignKey('Cargo', on_delete=models.CASCADE, related_name='cargos_dependientes')
    cargo_hijo = models.ForeignKey('Cargo', on_delete=models.CASCADE, related_name='cargos_superiores')

    def __str__(self):
        return f"{self.cargo_padre} → {self.cargo_hijo}"

