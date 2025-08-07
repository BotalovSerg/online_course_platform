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


class RoleDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def patch(self, request: HttpRequest, role_id: int):
        if not request.user.is_authenticated or request.user.role.name != "admin":
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response(
                {"error": "Role not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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


class BusinessElementDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def patch(self, request: HttpRequest, element_id: int):
        if not request.user.is_authenticated or request.user.role.name != "admin":
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            element = BusinessElement.objects.get(id=element_id)
        except BusinessElement.DoesNotExist:
            return Response(
                {"error": "BusinessElement not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BusinessElementSerializer(element, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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


class AccessRolesRuleDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def patch(self, request: HttpRequest, rule_id: int):
        if not request.user.is_authenticated or request.user.role.name != "admin":
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            rule = AccessRolesRule.objects.get(id=rule_id)
        except AccessRolesRule.DoesNotExist:
            return Response(
                {"error": "AccessRolesRule not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AccessRolesRuleSerializer(rule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
