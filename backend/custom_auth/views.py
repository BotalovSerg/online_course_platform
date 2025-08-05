import jwt
from datetime import datetime, timedelta, timezone

from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import UserSerializer


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
        if request.user and not isinstance(request.user, AnonymousUser):
            logout(request)
            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
