"""
   Users app models
"""
from django.db import models
from core.models import BaseModel, NameModel # pylint: disable=import-error


class TiposDoc(BaseModel):
    TIPO_CHOICES = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('RC', 'Registro civil'),
    ]
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    def __str__(self):
        return self.get_tipo_display()  # pylint: disable=no-member

class Generos(NameModel):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ]
    sigla = models.CharField(max_length=10, choices=GENERO_CHOICES)
    def __str__ (self):
        return self.get_sigla_display() # pylint: disable=no-member

class Usuarios(NameModel):
    apellido = models.CharField(max_length=255)
    num_doc = models.CharField(max_length=30, blank=False)
    tipo_doc = models.ForeignKey('users.TiposDoc', on_delete=models.DO_NOTHING)
    genero = models.ForeignKey('users.Generos', on_delete=models.DO_NOTHING)
    correo = models.EmailField(blank=False, unique=True)
    cargo = models.ForeignKey('cargos.Cargos', on_delete=models.DO_NOTHING)
    estudio_formal = models.ForeignKey('formacion.EstudioFormal', on_delete=models.DO_NOTHING)
    fecha_ingreso = models.DateField(auto_now=True)