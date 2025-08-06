from custom_auth.authentication import JWTAuthentication
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AccessRolesRule, BusinessElement, Role
from .serializers import (
    AccessRolesRuleSerializer,
    BusinessElementSerializer,
    RoleSerializer,
)


class RoleView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest):
        if not request.user.is_authenticated or request.user.role.name != "admin":
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN,
            )
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        if not request.user.is_authenticated or request.user.role.name != "admin":
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessElementView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest):
        if not request.user.is_authenticated or request.user.role.name != "admin":
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        elements = BusinessElement.objects.all()
        serializer = BusinessElementSerializer(elements, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        if not request.user.is_authenticated or request.user.role.name != "admin":
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        serializer = BusinessElementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessRolesRuleView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest):
        if not request.user.is_authenticated or request.user.role.name != "admin":
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        rules = AccessRolesRule.objects.all()
        serializer = AccessRolesRuleSerializer(rules, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        if not request.user.is_authenticated or request.user.role.name != "admin":
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        serializer = AccessRolesRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
