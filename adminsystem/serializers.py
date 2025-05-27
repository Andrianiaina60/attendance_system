from rest_framework import serializers
from .models import AdminSystem

class AdminSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSystem
        fields = '__all__'
