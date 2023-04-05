from rest_framework import serializers

from .models import Answer


class ProfessorAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "question", "student", "text", "attachment", "grade")
        read_only_fields = ("question", "student", "text", "attachment")
