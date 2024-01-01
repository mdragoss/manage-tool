from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from projects.urls import project_routes
from users.urls import user_routes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([*user_routes, *project_routes])),
    # Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
]
