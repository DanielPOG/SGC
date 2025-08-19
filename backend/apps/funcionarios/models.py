"""
    Modelos para el modulo de funcionarios 
    (Admin y el otro q no me acuerdoxd)
"""
from django.db import models
from core.models import BaseModel, NameModel # pylint: disable=import-error
from ckeditor.fields import RichTextField

class Bitacoras(BaseModel):
    usuario = models.ForeignKey("users.Usuarios", verbose_name=("autor"), on_delete=models.CASCADE)
    accion = RichTextField(("bitacora"), max_length=50)

class Red(NameModel):
    centro = models.ForeignKey("core.Centros", on_delete=models.CASCADE)

class Area(NameModel):
    red = models.ForeignKey("funcionarios.Red",on_delete=models.DO_NOTHING)