from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Authentication
from attendance.models import Employee


# Création compte (réservé admin)
class AuthRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    idemployee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Authentication
        fields = ['email', 'password', 'role', 'status', 'idemployee']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Authentication(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Sérialiseur pour login et token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        return token

# Profil utilisateur
class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authentication
        fields = ['email', 'role', 'status', 'idemployee']

# Changer email
class ChangeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authentication
        fields = ['email']

# Changer mot de passe
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
