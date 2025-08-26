from django.db import models
from core_apps.general.models import Centro #pylint:disable=import-error
from core_apps.usuarios_api.models import Usuario #pylint:disable=import-error

# Create your models here.
class EstadoGrupo(models.Model):
    estado = models.CharField(max_length=100)
class GrupoSena(models.Model):
    resolucion = models.CharField(max_length=200, primary_key=True)
    codigo_siga = models.CharField(max_length=200)
    nombre = models.CharField(max_length=100)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    estadoGrupo = models.ForeignKey('EstadoGrupo', on_delete=models.CASCADE)
    lider = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaActualizacion = models.DateTimeField(auto_now=True)

class UsuarioGrupo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    grupo = models.ForeignKey('GrupoSena', on_delete=models.CASCADE)
    fecha_i = models.DateTimeField(auto_now_add=True)
    fecha_r = models.DateTimeField(auto_now_add=False)
    resolucion = models.CharField(max_length=50)
    usuarioxcargo = models.ForeignKey('cargos_api.CargoUsuario', on_delete=models.RESTRICT)
