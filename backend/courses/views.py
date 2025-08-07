from custom_auth.authentication import JWTAuthentication
from custom_auth.models import GuestUser
from custom_rbac.models import AccessRolesRule
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Enrollment
from courses.serializers import CourseSerializer, EnrollmentSerializer


class CourseView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest):
        if request.user.is_anonymous:
            request.user = GuestUser()
        rule = AccessRolesRule.objects.filter(
            role=request.user.role,
            element__name="courses",
        ).first()
        if not rule or not (rule.read_permission or rule.read_all_permission):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        rule = AccessRolesRule.objects.filter(
            role=request.user.role,
            element__name="courses",
        ).first()
        if not rule or not rule.create_permission:
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(
            data=request.data,
            context={"creator": request.user},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        rule = AccessRolesRule.objects.filter(
            role=request.user.role,
            element__name="enrollments",
        ).first()
        if not rule or not (rule.read_permission or rule.read_all_permission):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        enrollments = (
            Enrollment.objects.filter(user=request.user)
            if not rule.read_all_permission
            else Enrollment.objects.all()
        )
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        rule = AccessRolesRule.objects.filter(
            role=request.user.role,
            element__name="enrollments",
        ).first()
        if not rule or not rule.create_permission:
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer = EnrollmentSerializer(
            data=request.data,
            context={"user": request.user},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
