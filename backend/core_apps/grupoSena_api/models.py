from django.db import models
from core_apps.usuarios_api.models import Usuario
from core_apps.general.models import Area
from django.utils import timezone



class EstadoGrupo(models.Model):
    estado = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.estado


class NombreGrupo(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Grupo")

    def __str__(self):
        return self.nombre


class GrupoSena(models.Model):
    nombre = models.ForeignKey(
        NombreGrupo,
        on_delete=models.PROTECT,
        verbose_name="Nombre del Grupo",
    )
    area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name="Área Funcional")
    capacidad = models.PositiveIntegerField(verbose_name="Capacidad Máxima")
    lider = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grupos_dirigidos',
        verbose_name="Líder del Grupo"
    )
    resolucion1 = models.CharField( 
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nombre de Resolución"
    )
    resolucion2 = models.FileField(
        upload_to='resolucionesGrupoUsuario/',
        null=True,
        blank=True,
        verbose_name="Resolución 2"
    )
    fecha_creacion = models.DateField(
            auto_now_add=True,
            verbose_name="Fecha de Creación"
        )


    
    observacion = models.TextField(blank=True, null=True, verbose_name="Observación")
    estado = models.ForeignKey(
        EstadoGrupo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Estado del Grupo"
    )

    def __str__(self):
        nombre = self.nombre.nombre if self.nombre else "Sin nombre"
        return f"{nombre} - {self.area}"

class UsuarioGrupo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    grupo = models.ForeignKey(GrupoSena, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_salida = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('usuario', 'grupo')

    def __str__(self):
        return f"{self.usuario} - {self.grupo}"
