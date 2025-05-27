"""
URL configuration for attendance_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema view configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Attendance API",
        default_version='v1',
        description="API pour la gestion de l'assiduité des employés avec reconnaissance faciale",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@company.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # App APIs
    path('api/', include('attendance.urls')),           # Pointage et employés
    path('api/adminsystem/', include('adminsystem.urls')),  # Gestion système administrateur
    path('api/leave/', include('leave.urls')),          # Gestion des congés
    path('api/auth/', include('authentication.urls')), # Include authentication URLs

    # Documentation Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
