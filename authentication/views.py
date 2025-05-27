from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import (
    AuthRegisterSerializer,
    MyTokenObtainPairSerializer,
    AuthUserSerializer,
    ChangeEmailSerializer,
    ChangePasswordSerializer,
)
from .models import Authentication

# Endpoint création compte (admin uniquement)
class RegisterView(generics.CreateAPIView):
    queryset = Authentication.objects.all()
    serializer_class = AuthRegisterSerializer
    permission_classes = [permissions.IsAdminUser]

# Login + refresh
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Profil (employé authentifié)
class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuthUserSerializer

    def get_object(self):
        return self.request.user

# Changer email
class ChangeEmailView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def get_object(self):
        return self.request.user

# Changer mot de passe
class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Mot de passe mis à jour avec succès."}, status=status.HTTP_200_OK)
