""" 
    Modelos para app de 
    formacion de funcionario
"""
from django.db import models
from core.models import BaseModel, NameModel # pylint: disable=import-error

class EstudioFormal(BaseModel):
    nombre = models.CharField(max_length=50)

class Completementaria(NameModel):
    tipo = models.CharField(("tipo_fcomplementaria"), max_length=100)
    usuario = models.ForeignKey("users.Usuarios", on_delete=models.CASCADE)