# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update-profile'),
]

# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5MDc1NDcyLCJpYXQiOjE3NDkwMzk0NzIsImp0aSI6ImMzYmFkZDYzZTVlNTQ0MmM4OWE4OTE1MTdhOGY2NzJiIiwidXNlcl9pZCI6M30.Dr7cAzenpGT7c7rtVRwbnWHMYMST4sAKG-UqNVNfPzU"
# http://127.0.0.1:8000/api/auth/profile/


# from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenBlacklistView,
#     TokenVerifyView,
# )
# from . import views

# urlpatterns = [
#     # JWT Endpoints
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
#     path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    
#     # Autres endpoints d'authentification
#     path('profile/', views.ProfileView.as_view(), name='profile'),
#     path('register/', views.RegisterView.as_view(), name='register'),
#     # ... autres vues
# ]