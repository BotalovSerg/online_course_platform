from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone

from .models import CustomUser


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = CustomUser.objects.get(email=email, is_active=True)
            if user.check_password(password):

                token = jwt.encode(
                    {
                        "user_id": user.id,
                        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
                    },
                    settings.JWT_SECRET,
                    algorithm="HS256",
                )
                return Response({"token": token}, status=status.HTTP_200_OK)
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
