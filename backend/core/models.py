""" 
    Modelo básico base con abstracción 
    para modelos simples 
"""
import uuid
from django.db import models

class BaseModel (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Estados(BaseModel):
    nombre = models.CharField( max_length=50)

class Regionales(BaseModel):
    nombre = models.CharField(max_length=255)

class NameModel(BaseModel):
    nombre = models.CharField(max_length=250)
    class Meta:
        abstract=True

class Centros(NameModel):
    regional = models.ForeignKey('core.Regionales', on_delete=models.CASCADE)