# signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Usuario
from core_apps.cargos_api.models import   CargoUsuario, EstadoVinculacion

# Guardamos temporalmente el cargo anterior del usuario antes de actualizar
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
    # 🚨 Evitar que el superuser quede en CargoUsuario
    if instance.is_superuser:
        return  

    cargo_anterior = _usuario_cargo_anterior.pop(instance.pk, None)

    # Caso 1: Usuario recién creado
    if created and instance.cargo:
        CargoUsuario.objects.create(
            cargo=instance.cargo,
            usuario=instance,
            salario=0,
            grado=1,
            resolucion=instance.resolucion,
            estadoVinculacion=EstadoVinculacion.objects.get(estado="PLANTA")
        )

    # Caso 2: Usuario actualizado y cambió de cargo
    elif not created and instance.cargo_id != cargo_anterior:
        # 2.1 Cerrar el registro anterior
        ultimo_cargo = CargoUsuario.objects.filter(
            usuario=instance,
            cargo_id=cargo_anterior,
            fechaRetiro__isnull=True
        ).order_by('-fechaInicio').first()

        if ultimo_cargo:
            ultimo_cargo.fechaRetiro = now().date()
            ultimo_cargo.save()

        # 2.2 Crear el nuevo registro
        CargoUsuario.objects.create(
            cargo=instance.cargo,
            usuario=instance,
            salario=0,
            grado=1,
            resolucion=instance.resolucion,
            estadoVinculacion=EstadoVinculacion.objects.get(estado="PLANTA")
        )
