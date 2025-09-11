import threading

# Thread-local para almacenar datos por request
_user_local = threading.local()

def get_current_user():
    """Permite obtener el usuario actual en cualquier parte del código (signals, etc)."""
    return getattr(_user_local, "user", None)

class CurrentUserMiddleware:
    """Middleware para guardar el request.user en thread-local."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user_local.user = getattr(request, "user", None)
        response = self.get_response(request)
        _user_local.user = None  # Limpieza después de la petición
        return response
