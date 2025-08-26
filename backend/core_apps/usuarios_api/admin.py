from django.contrib import admin
from .models import TipoDocumento, Genero, EstudioFormal, Rol, Estado, UsuarioManager, Usuario
# Register your models here.
admin.site.register(Usuario)
admin.site.register(TipoDocumento)
admin.site.register(Genero)
admin.site.register(EstudioFormal)
admin.site.register(Rol)
admin.site.register(Estado)
admin.site.register(UsuarioManager)
