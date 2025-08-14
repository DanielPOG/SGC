"""
    Database models
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
    
class EstadosGrupo(BaseModel):
    nombre = models.CharField(max_length=50)

class EstudioFormal(BaseModel):
    nombre = models.CharField(max_length=50)

class TiposDoc(BaseModel):
    TIPO_CHOICES = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('RC', 'Registro civil'),
    ]
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    def __str__(self):
        return self.get_tipo_display()
    
class Generos(BaseModel):
    class GeneroSiglas(models.TextChoices):
        M = 'M', 'Masculino'
        F = 'F', 'Femenino'
        OTRO = 'OTRO', 'Otros'
    nombre = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10, choices=GeneroSiglas.choices)

class NombresCargo(BaseModel):
    nombre = models.CharField(max_length=100, unique=True)
    
class Cargos(BaseModel):
    idp = models.CharField(max_length=50)
    resolucion = models.CharField( max_length=50)
    nombre = models.ForeignKey("users.NombresCargo", on_delete=models.CASCADE)
    
    

class Usuarios(BaseModel):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    num_doc = models.CharField(max_length=30, blank=False)