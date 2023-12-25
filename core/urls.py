"""
# webapp/core/urls.py
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Temple Address API",
        default_version='v1',
        description="REST API Endpoints for Temple and Service Listing",
        terms_of_service="https://www.templeaddress.com/terms/",
        contact=openapi.Contact(email="info@vasssystems.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/user/', include("user.urls", namespace='user')),
    path('api/v1/features/', include("features.urls", namespace='features')),
    path('api/v1/utils/', include("utils.urls", namespace='utils')),
    # path('api/v1/adminapp/', include("adminapp.urls", namespace='adminapp')),
    path('api/v1/cms/', include("cms.urls", namespace='cms')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('', include("utils.urls", namespace='utils')),
]