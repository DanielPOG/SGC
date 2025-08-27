from django.contrib import admin
from .models import (Usuario,TipoDocumento,Genero,EstudioFormal,Rol,Estado,
                    UsuarioManager,TipoCertificado,
                    FormacionComplementaria,Bitacora,EstadoSolicitud,TipoSolicitud)
# Register your models here.
admin.site.register(Usuario)
admin.site.register(TipoDocumento)
admin.site.register(Genero)
admin.site.register(EstudioFormal)
admin.site.register(Rol)
admin.site.register(Estado)
admin.site.register(TipoCertificado)
admin.site.register(FormacionComplementaria)
admin.site.register(Bitacora)
admin.site.register(EstadoSolicitud)
admin.site.register(TipoSolicitud)
