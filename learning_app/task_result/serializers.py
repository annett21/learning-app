from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Answer


class ProfessorAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ("question", "student", "text", "attachment")


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ("student", "grade")

    def validate(self, attrs):
        if self.instance is None:
            question_course = attrs["question"].task.course
            student = self.context["request"].user
            allowed_courses = student.studied_courses.all()
            if question_course not in allowed_courses:
                err = "The question doesn't belong to user's courses"
                raise ValidationError(err)
        return attrs

    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user
        return super().create(validated_data)


class StudentAnswerUpdateSerializer(StudentAnswerSerializer):
    class Meta(StudentAnswerSerializer.Meta):
        read_only_fields = StudentAnswerSerializer.Meta.read_only_fields + (
            "question",
        )
