from django.contrib import admin
from .models import CargoNombre,EstadoCargo,Cargo,CargoUsuario, Idp, EstadoVinculacion
# Register your models here.
from django.contrib import admin



# ======================
# IDP
# ======================
@admin.register(Idp)
class IdpAdmin(admin.ModelAdmin):
    list_display = ("id", "numero", "fechaCreacion")
    search_fields = ("numero",)
    list_filter = ("fechaCreacion",)
    date_hierarchy = "fechaCreacion"
    ordering = ("-fechaCreacion",)


# ======================
# CargoNombre
# ======================
@admin.register(CargoNombre)
class CargoNombreAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "funcion")  # ahora mostramos también la función
    search_fields = ("nombre", "funcion")


# ======================
# EstadoCargo
# ======================
@admin.register(EstadoCargo)
class EstadoCargoAdmin(admin.ModelAdmin):
    list_display = ("id", "estado")
    search_fields = ("estado",)


# ======================
# EstadoVinculacion
# ======================
@admin.register(EstadoVinculacion)
class EstadoVinculacionAdmin(admin.ModelAdmin):
    list_display = ("id", "estado")
    search_fields = ("estado",)


# ======================
# Inlines
# ======================
class CargoUsuarioInline(admin.TabularInline):
    model = CargoUsuario
    extra = 0
    can_delete = True
    verbose_name_plural = "Asignaciones de Usuario"


# ======================
# Cargo
# ======================
@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("idp", "cargoNombre", "estadoCargo", "centro", "fechaCreacion", "fechaActualizacion")
    search_fields = ("idp__numero", "cargoNombre__nombre", "centro__nombre")
    list_filter = ("estadoCargo", "centro", "fechaCreacion")
    date_hierarchy = "fechaCreacion"
    ordering = ("-fechaCreacion",)
    inlines = [CargoUsuarioInline]  # quitamos CargoFuncionInline porque ya no aplica


# ======================
# CargoUsuario
# ======================
@admin.register(CargoUsuario)
class CargoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "cargo", "usuario", "salario", "grado", "resolucion", "fechaInicio", "fechaRetiro")
    search_fields = ("cargo__idp__numero", "usuario__username")
    list_filter = ("grado", "fechaInicio", "fechaRetiro")
    date_hierarchy = "fechaInicio"
