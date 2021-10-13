from django.contrib import admin
from django.urls import path , re_path
from django.urls.conf import include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Simple WeatherStack API With django",
        default_version='v1',
        description="Swagger documentation for project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="imanhpr1999@gmail.com"),
        license=openapi.License(name="Free License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
        cache_timeout=0), name='schema-swagger-ui'),
]
