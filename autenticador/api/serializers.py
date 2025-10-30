from rest_framework import serializers
from autenticador.models import Box, CustomUser

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ["things"]

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "password", "email", "rights"]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, default=None)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(default=None)