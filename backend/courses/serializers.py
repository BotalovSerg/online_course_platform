from rest_framework import serializers

from courses.models import Course, Enrollment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "description", "price", "creator", "created_at"]
        extra_kwargs = {
            "creator": {
                "required": False,
            }
        }
        read_only_fields = ("creator",)

    def create(self, validated_data):
        validated_data["creator"] = self.context.get("creator")
        return super().create(validated_data)


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "user", "course", "enrolled_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("user")
        return super().create(validated_data)
