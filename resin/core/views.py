from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import AuthLoginSerializer, AuthLogoutSerializer, UserProfileSerializer, DetailSerializer


User = get_user_model()


class AuthViewSet(GenericViewSet):
    @csrf_exempt
    @extend_schema(
        tags=["auth"],
        responses={
            200: DetailSerializer,
            400: DetailSerializer,
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="login",
        serializer_class=AuthLoginSerializer,
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def login(self, request):
        validated_data = self.get_serializer(data=request.data)
        validated_data.is_valid(raise_exception=True)

        user = authenticate(
            email=validated_data.validated_data["email"],
            password=validated_data.validated_data["password"],
        )

        if user is None:
            response_serializer = DetailSerializer({"detail": _("Invalid credentials")})
            return Response(response_serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            login(request, user)
            response_serializer = DetailSerializer({"detail": _("Logged in successfully")})
            return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["auth"],
        responses={
            200: DetailSerializer,
        },
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="logout",
        serializer_class=AuthLogoutSerializer,
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        logout(request)
        response_serializer = DetailSerializer({"detail": _("Logged out successfully")})
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class UserViewSet(GenericViewSet):
    @extend_schema(
        tags=["users"],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        serializer_class=UserProfileSerializer,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        return Response(self.get_serializer(request.user).data)
