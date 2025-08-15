"""
    Modelos app cargos
"""
from django.db import models
from core.models import BaseModel # pylint: disable=import-error

class NombresCargo(BaseModel):
    nombre = models.CharField(max_length=100, unique=True)

class Cargos(BaseModel):
    idp = models.CharField(max_length=50)
    resolucion = models.CharField( max_length=150)
    nombre = models.ForeignKey("cargos.NombresCargo", on_delete=models.CASCADE)
    estado = models.ForeignKey("core.Estados", on_delete=models.DO_NOTHING)

class UsuariosCargo(BaseModel):
    cargo = models.ForeignKey("cargos.Cargos", on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey('users.Usuarios', on_delete=models.DO_NOTHING)
    fecha_asignacion = models.DateField(blank=False)
    fecha_fin = models.DateField(blank=False)
    grado = models.CharField(max_length=255)