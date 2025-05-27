from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    MyTokenObtainPairView,
    ProfileView,
    ChangeEmailView,
    ChangePasswordView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),       # Création compte par admin uniquement
    path('login/', MyTokenObtainPairView.as_view(), name='auth_login'),    # Login utilisateur
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),     # Rafraîchir token
    path('profile/', ProfileView.as_view(), name='auth_profile'),          # Voir profil
    path('change-email/', ChangeEmailView.as_view(), name='auth_change_email'), # Modifier email
    path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'), # Modifier mot de passe
]
