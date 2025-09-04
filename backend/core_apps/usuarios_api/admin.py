from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, TipoDocumento, Genero, EstudioFormal, Rol, Estado,
    TipoCertificado, FormacionComplementaria, Bitacora,
    EstadoSolicitud, TipoSolicitud, Solicitud
)

# --- Inlines ---
class FormacionComplementariaInline(admin.TabularInline):
    model = FormacionComplementaria
    extra = 0
    fields = ('nombre', 'tipo', 'institucion', 'fechaInicio', 'fechaFin', 'certificado_link')
    readonly_fields = ('certificado_link',)

    def certificado_link(self, obj):
        if obj and obj.certificado:
            return format_html('<a href="{}" target="_blank">Ver certificado</a>', obj.certificado.url)
        return "-"

# --- Usuario Admin ---
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('correo', 'nombre', 'apellido', 'tipo_doc', 'num_doc', 'cargo', 'estado', 'is_staff', 'is_active')
    search_fields = ('correo', 'nombre', 'apellido', 'num_doc')
    list_filter = ('estado', 'cargo', 'genero', 'rol', 'is_staff', 'is_active')
    ordering = ('correo',)
    inlines = [FormacionComplementariaInline]

    fieldsets = (
        ('Credenciales', {'fields': ('correo', 'password')}),
        ('Datos personales', {'fields': ('nombre', 'apellido', 'tipo_doc', 'num_doc', 'genero', 'fecha_n')}),
        ('Organización', {'fields': ('cargo', 'estudioF', 'rol', 'estado', 'dependencia', 'software')}),
        ('Fechas', {'fields': ('fechaInicio', 'fechaActualizacion', 'fechaRetiro')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Sesiones', {'fields': ('last_login',)}),
    )
    readonly_fields = ('fechaInicio', 'fechaActualizacion', 'last_login')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre', 'apellido', 'num_doc','fecha_n', 'password1', 'password2',
                       'tipo_doc', 'genero', 'cargo', 'estudioF', 'rol', 'estado', 'dependencia', 'software'),
        }),
    )

# --- Catálogos ---
@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nombre')
    search_fields = ('sigla', 'nombre')

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nombre')
    search_fields = ('sigla', 'nombre')

@admin.register(EstudioFormal)
class EstudioFormalAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# --- Formaciones y bitácora ---
@admin.register(TipoCertificado)
class TipoCertificadoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(FormacionComplementaria)
class FormacionComplementariaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'tipo', 'institucion', 'fechaInicio', 'fechaFin')
    search_fields = ('nombre', 'usuario__correo', 'institucion')
    list_filter = ('tipo', 'institucion', 'fechaInicio', 'fechaFin')
    readonly_fields = ()

@admin.register(Bitacora)
class BitacoraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha')
    search_fields = ('usuario__correo', 'accion')
    list_filter = ('fecha',)
    date_hierarchy = 'fecha'

# --- Solicitudes ---
@admin.register(EstadoSolicitud)
class EstadoSolicitudAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(TipoSolicitud)
class TipoSolicitudAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'emisor', 'receptor', 'tipo', 'estado', 'fechaCreacion', 'fechaAprobada')
    search_fields = ('emisor__correo', 'receptor__correo', 'descripcion')
    list_filter = ('tipo', 'estado', 'fechaCreacion', 'fechaAprobada')
    date_hierarchy = 'fechaCreacion'
