# signals.py
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

from .models import Usuario, Bitacora, Accion
from core_apps.cargos_api.models import CargoUsuario, EstadoVinculacion
from core_apps.usuarios_api.middleware import get_current_user

# --------------------------
# 🔹 BITÁCORA (GENÉRICO) TODO:PONER CUANDO YA HAYA INICIO DE SESION 
# --------------------------
# _pre_save_cache = {}

# @receiver(pre_save)
# def cache_before_update(sender, instance, **kwargs):
#     if sender == Bitacora:
#         return
#     if not sender._meta.app_label.startswith("django"):
#         if instance.pk:
#             try:
#                 old = sender.objects.get(pk=instance.pk)
#                 _pre_save_cache[(sender, instance.pk)] = old
#             except sender.DoesNotExist:
#                 pass

# @receiver(post_save)
# def registrar_crear_actualizar(sender, instance, created, **kwargs):
#     if sender == Bitacora:
#         return
#     if not sender._meta.app_label.startswith("django"):
#         usuario = get_current_user()
#         if not usuario or usuario.software != 2:
#             return  

#         content_type = ContentType.objects.get_for_model(sender)

#         if created:
#             Bitacora.objects.create(
#                 usuario=usuario,
#                 accion=Accion.CREAR,
#                 content_type=content_type,
#                 object_id=str(instance.pk),
#                 descripcion=f"Se creó un registro en {sender.__name__}"
#             )
#         else:
#             cambios = {}
#             old = _pre_save_cache.pop((sender, instance.pk), None)
#             if old:
#                 for field in sender._meta.fields:
#                     nombre = field.name
#                     old_val, new_val = getattr(old, nombre), getattr(instance, nombre)
#                     if old_val != new_val:
#                         cambios[nombre] = [old_val, new_val]

#             Bitacora.objects.create(
#                 usuario=usuario,
#                 accion=Accion.ACTUALIZAR,
#                 content_type=content_type,
#                 object_id=str(instance.pk),
#                 cambios=cambios or None,
#                 descripcion=f"Se actualizó un registro en {sender.__name__}"
#             )

# @receiver(post_delete)
# def registrar_eliminar(sender, instance, **kwargs):
#     if sender == Bitacora:
#         return
#     if not sender._meta.app_label.startswith("django"):
#         usuario = get_current_user()
#         if not usuario or usuario.software != 2:
#             return  

#         content_type = ContentType.objects.get_for_model(sender)
#         Bitacora.objects.create(
#             usuario=usuario,
#             accion=Accion.ELIMINAR,
#             content_type=content_type,
#             object_id=str(instance.pk),
#             descripcion=f"Se eliminó un registro en {sender.__name__}"
#         ) 




# --------------------------
# 🔹 USUARIO Y CARGOS
# --------------------------
_usuario_cargo_anterior = {}

@receiver(pre_save, sender=Usuario)
def guardar_cargo_anterior(sender, instance, **kwargs):
    if instance.pk:  # si el usuario ya existe en BD
        try:
            anterior = Usuario.objects.get(pk=instance.pk)
            _usuario_cargo_anterior[instance.pk] = anterior.cargo_id
        except Usuario.DoesNotExist:
            _usuario_cargo_anterior[instance.pk] = None

@receiver(post_save, sender=Usuario)
def manejar_cargo_usuario(sender, instance, created, **kwargs):
    if instance.is_superuser:  # 🚨 Evitar que el superuser quede en CargoUsuario
        return  

    if created and instance.cargo:
        # Solo cuando el usuario se crea con un cargo PLANTA
        CargoUsuario.objects.create(
            cargo=instance.cargo,
            usuario=instance,
            salario=0,
            grado=1,
            resolucion=instance.resolucion,
            estadoVinculacion=EstadoVinculacion.objects.get(estado="PLANTA")
        )
