from django.urls import path

from .views import CourseView, EnrollmentView

urlpatterns = [
    path("courses/", CourseView.as_view(), name="courses"),
    path("enrollment/", EnrollmentView.as_view(), name="enrollment"),
]
