from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import para JWT login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('core_apps.usuarios_api.urls')), 
    path('api/cargos/', include('core_apps.cargos_api.urls')),
    path('api/gruposena/', include('core_apps.grupoSena_api.urls')),
    path('api/general/', include('core_apps.general.urls')),

    # Login con JWT
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
