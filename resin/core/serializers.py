from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class DetailSerializer(serializers.Serializer):
    detail = serializers.CharField()


class AuthLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AuthLogoutSerializer(serializers.Serializer):
    pass


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "is_staff", "is_superuser", "last_login"]
