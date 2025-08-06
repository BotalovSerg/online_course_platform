from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import JWTAuthentication
from .models import CustomUser
from .serializers import ProfileSerializer, UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered",
                    "user_id": user.pk,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    def post(self, request: HttpRequest):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = CustomUser.objects.get(email=email, is_active=True)
            if user.check_password(password):
                token = jwt.encode(
                    {
                        "user_id": user.pk,
                        "email": user.email,
                        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
                    },
                    settings.JWT_SECRET,
                    algorithm="HS256",
                )
                return Response(
                    {"token": token},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        request.user.is_active = False
        request.user.save()
        logout(request)
        return Response(
            {"message": "Account deactivated, please log out"},
            status=status.HTTP_200_OK,
        )
