from django.contrib import admin
from .models import CargoNombre,EstadoCargo,Cargo,CargoFuncion,CargoUsuario
# Register your models here.
@admin.register(CargoNombre)
class CargoNombreAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(EstadoCargo)
class EstadoCargoAdmin(admin.ModelAdmin):
    list_display = ("id", "estado")
    search_fields = ("estado",)


class CargoFuncionInline(admin.TabularInline):
    model = CargoFuncion
    extra = 1  # cantidad de formularios vacíos que aparecen


class CargoUsuarioInline(admin.TabularInline):
    model = CargoUsuario
    extra = 1


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("idp", "cargoNombre", "estadoCargo", "centro", "fechaCreacion", "fechaActualizacion")
    search_fields = ("idp", "cargoNombre__nombre", "centro__nombre")
    list_filter = ("estadoCargo", "centro", "fechaCreacion")
    date_hierarchy = "fechaCreacion"
    ordering = ("-fechaCreacion",)
    inlines = [CargoFuncionInline, CargoUsuarioInline]


@admin.register(CargoFuncion)
class CargoFuncionAdmin(admin.ModelAdmin):
    list_display = ("id", "cargo", "funcion")
    search_fields = ("cargo__idp", "funcion")


@admin.register(CargoUsuario)
class CargoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "cargo", "usuario", "salario", "grado", "resolucion", "fechaInicio", "fechaRetiro")
    search_fields = ("cargo__idp", "usuario__username")
    list_filter = ("grado", "fechaInicio", "fechaRetiro")
    date_hierarchy = "fechaInicio"
