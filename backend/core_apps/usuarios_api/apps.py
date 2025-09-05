from django.apps import AppConfig


class UsuariosApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_apps.usuarios_api'
    
    def ready(self):
        import core_apps.usuarios_api.signals
