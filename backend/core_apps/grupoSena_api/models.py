from django.db import models
from general.models import Centro
from usuarios_api.models import Usuario

# Create your models here.
class EstadoGrupo(models.Model):
    estado = models.CharField(max_length=100)
class GrupoSena(models.Model):
    resolucion = models.CharField(max_length=200)
    nombre = models.CharField(max_length=100)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    estadoGrupo = models.ForeignKey('EstadoGrupo', on_delete=models.CASCADE)
    lider = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaActualizacion = models.DateTimeField(auto_now=True)
class UsuarioGrupo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    grupo = models.ForeignKey('GrupoSena', on_delete=models.CASCADE)