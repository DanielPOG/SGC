from django.contrib import admin
from .models import EstadoCargo, Cargo, CargoFuncion, CargoNombre, CargoUsuario
# Register your models here.
admin.site.register(EstadoCargo)
admin.site.register(Cargo)
admin.site.register(CargoFuncion)
admin.site.register(CargoNombre)
admin.site.register(CargoUsuario)
