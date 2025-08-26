from django.contrib import admin
from .models import CargoNombre,EstadoCargo,Cargo,CargoFuncion,CargoUsuario
# Register your models here.
admin.site.register(CargoNombre)
admin.site.register(EstadoCargo)
admin.site.register(Cargo)
admin.site.register(CargoFuncion)
admin.site.register(CargoUsuario)
