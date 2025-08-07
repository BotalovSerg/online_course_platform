import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status

from .models import CustomUser, GuestUser


class JWTMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        request.user = GuestUser()
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
                user = CustomUser.objects.get(id=payload["user_id"], is_active=True)
                request.user = user
            except (
                jwt.InvalidTokenError,
                jwt.ExpiredSignatureError,
                CustomUser.DoesNotExist,
            ):
                return JsonResponse(
                    {"error": "Unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return self.get_response(request)
