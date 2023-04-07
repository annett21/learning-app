from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Answer, Result


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
        student = self.context["request"].user
        task = attrs["question"].task

        if Result.objects.filter(student=student, task=task).exists():
            err = "You cannot change an answer after submition for review."
            raise ValidationError(err)

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


class ProfessorResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"
        read_only_fields = ("task", "student")


class StudentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"
        read_only_fields = ("grade", "student")

    def validate(self, attrs):
        student = self.context["request"].user
        task = attrs["task"]

        if Result.objects.filter(student=student, task=task).exists():
            err = "You cannot submit a task for review a second time."
            raise ValidationError(err)

        deadline = task.end_at
        if deadline and timezone.now() > deadline:
            raise ValidationError("The task fulfillment time has expired.")

        return attrs

    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user
        return super().create(validated_data)
