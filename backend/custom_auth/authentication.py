import jwt
from django.conf import settings
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request: HttpRequest):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("user_id")
            user = CustomUser.objects.get(id=user_id, is_active=True)

        except (
            jwt.InvalidTokenError,
            jwt.ExpiredSignatureError,
            CustomUser.DoesNotExist,
        ):
            raise AuthenticationFailed("Invalid token")

        return (user, None)
