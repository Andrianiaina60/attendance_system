
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
    path('api/leave/', include('leave.urls')),          # Gestion des congés
    path('api/auth/', include('authentication.urls')), # Include authentication URLs

    # Documentation Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]



# ACTIVATE ENVIRONNEMENT:
#     .\env310\Scripts\Activate.ps1




# """
# URL configuration for attendance_system project.
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.1/topics/http/urls/
# """
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from django.http import JsonResponse
# from django.utils import timezone

# # Swagger schema view configuration
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Attendance System API",
#         default_version='v1',
#         description="API complète pour la gestion de l'assiduité des employés avec reconnaissance faciale",
#         terms_of_service="https://www.yourcompany.com/terms/",
#         contact=openapi.Contact(email="contact@company.com"),
#         license=openapi.License(name="MIT License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

# urlpatterns = [
#     # ========================================
#     # Django Administration
#     # ========================================
#     path('admin/', admin.site.urls),
    
#     # ========================================
#     # Application APIs
#     # ========================================
#     # Authentication app (inclut login, register, profile, JWT tokens, etc.)
#     path('api/auth/', include('authentication.urls')),
    
#     # Attendance app (pointage, employés, statistiques)
#     path('api/', include('attendance.urls')),
    
#     # Leave app (demandes de congés)
#     path('api/leave/', include('leave.urls')),
    
#     # ========================================
#     # API Documentation
#     # ========================================
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
#     # ========================================
#     # Health Check (optionnel mais recommandé)
#     # ========================================
#     path('api/health/', include([
#         path('', lambda request: JsonResponse({'status': 'ok', 'timestamp': timezone.now().isoformat()})),
#     ])),
# ]

# # ========================================
# # Servir les fichiers statiques et media en développement
# # ========================================
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
#     # Optionnel: Debug Toolbar pour le développement
#     try:
#         import debug_toolbar
#         urlpatterns = [
#             path('__debug__/', include(debug_toolbar.urls)),
#         ] + urlpatterns
#     except ImportError:
#         pass
