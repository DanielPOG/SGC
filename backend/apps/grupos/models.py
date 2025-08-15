"""
    Modelos Grupo Sena 
    //Posible movimiento a la app funcionarios
"""
from django.db import models
from core.models import BaseModel, NameModel # pylint: disable=import-error


class EstadosGrupo(BaseModel):
    nombre = models.CharField(max_length=50)

class Grupos(NameModel):
    centro = models.ForeignKey("core.Centros", on_delete=models.CASCADE)
    estado = models.ForeignKey("grupos.EstadosGrupo", on_delete=models.CASCADE)
    lider = models.ForeignKey("users.Usuarios", on_delete=models.CASCADE)
    resolucion = models.CharField(max_length=100)
    
class UsuariosGrupo(BaseModel):
    usuario = models.ForeignKey("users.Usuarios", on_delete=models.CASCADE)
    grupo = models.ForeignKey("grupos.Grupos", on_delete=models.DO_NOTHING)