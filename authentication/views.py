# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee
from .serializers import (
    EmployeeSerializer, 
    LoginSerializer, 
    EmployeeRegistrationSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Connexion d'un employé
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Informations utilisateur
        user_data = EmployeeSerializer(user).data
        
        return Response({
            'success': True,
            'message': 'Connexion réussie',
            'user': user_data,
            'tokens': {
                'access': str(access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Inscription d'un nouvel employé
    """
    serializer = EmployeeRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        employee = serializer.save()
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(employee)
        access_token = refresh.access_token
        
        user_data = EmployeeSerializer(employee).data
        
        return Response({
            'success': True,
            'message': 'Inscription réussie',
            'user': user_data,
            'tokens': {
                'access': str(access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Déconnexion d'un employé
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'success': True,
            'message': 'Déconnexion réussie'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Erreur lors de la déconnexion'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Récupération du profil de l'employé connecté
    """
    user_data = EmployeeSerializer(request.user).data
    return Response({
        'success': True,
        'user': user_data
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """
    Mise à jour du profil de l'employé connecté
    """
    serializer = EmployeeSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Profil mis à jour avec succès',
            'user': serializer.data
        })
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)