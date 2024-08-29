from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

# Set up the schema view for Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="RoomPriceGenie API",
      default_version='v1',
      description="API documentation for RoomPriceGenie services",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@roompricegenie.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('data_provider.api.urls')),  # Include data_provider URLs
    path('api/', include('dashboard.api.urls')),      # Include dashboard URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI
]
