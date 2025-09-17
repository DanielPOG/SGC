from django.contrib import admin
from .models import Regional, Centro, Red, Area, Dependencia
# Register your models here.
class CentroInline(admin.TabularInline):
    model = Centro
    extra = 1


class RedInline(admin.TabularInline):
    model = Red
    extra = 1


class AreaInline(admin.TabularInline):
    model = Area
    extra = 1


@admin.register(Regional)
class RegionalAdmin(admin.ModelAdmin):
    list_display = ("codigoRegional", "nombre")
    search_fields = ("codigoRegional", "nombre")
    ordering = ("nombre",)
    inlines = [CentroInline]


@admin.register(Centro)
class CentroAdmin(admin.ModelAdmin):
    list_display = ("codigoCentro", "nombre", "regional")
    search_fields = ("codigoCentro", "nombre", "regional__nombre")
    list_filter = ("regional",)
    ordering = ("nombre",)
    inlines = [RedInline]


@admin.register(Red)
class RedAdmin(admin.ModelAdmin):
    list_display = ("codigoRed", "nombre", "centro")
    search_fields = ("codigoRed", "nombre", "centro__nombre")
    list_filter = ("centro",)
    ordering = ("nombre",)
    inlines = [AreaInline]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("codigoArea", "nombre", "red")
    search_fields = ("codigoArea", "nombre", "red__nombre")
    list_filter = ("red",)
    ordering = ("nombre",)


@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    list_display = ("codigoDependencia", "nombre")
    search_fields = ("codigoDependencia", "nombre")
    ordering = ("nombre",)