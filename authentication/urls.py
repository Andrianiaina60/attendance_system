# urls.py
from django.urls import path
from .views import RegisterView, UserListView, CustomTokenObtainPairView, ChangePasswordView, UpdateEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('update-email/', UpdateEmailView.as_view(), name='update-email'),
]
