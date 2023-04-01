from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "professor", "students", "max_students")
        read_only_fields = ("professor", "students")

    def create(self, validated_data):
        validated_data["professor"] = self.context["request"].user
        return super().create(validated_data)
