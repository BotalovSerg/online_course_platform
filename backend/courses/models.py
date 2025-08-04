from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        "custom_auth.CustomUser",
        on_delete=models.CASCADE,
        related_name="created_courses",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "courses_course"


class Enrollment(models.Model):
    user = models.ForeignKey(
        "custom_auth.CustomUser",
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.course.name}"

    class Meta:
        db_table = "courses_enrollment"
        unique_together = ("user", "course")
