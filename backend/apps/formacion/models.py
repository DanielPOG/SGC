""" 
    Modelos para app de 
    formacion de funcionario
"""
from django.db import models
from apps.core.models import BaseModel, NameModel # pylint: disable=import-error

class EstudioFormal(BaseModel):
    nombre = models.CharField(max_length=50)

class Complementaria(NameModel):
    tipo = models.CharField(("tipo_fcomplementaria"), max_length=100)
    usuario = models.ForeignKey("users.Usuarios", on_delete=models.CASCADE)
    institucion = models.CharField( max_length=100)
    certificado = models.CharField( max_length=100)
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField(auto_now=False, auto_now_add=False)