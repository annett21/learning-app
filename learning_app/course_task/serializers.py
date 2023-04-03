from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Question, Task


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "text")

    def to_internal_value(self, data):
        return Question(**data)


class TaskSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ("id", "title", "course", "start_at", "end_at", "questions")

    def validate(self, attrs):
        start_at = attrs.get("start_at") or getattr(
            self.instance, "start_at", None
        )
        end_at = attrs.get("end_at") or getattr(self.instance, "end_at", None)
        if start_at and end_at and start_at >= end_at:
            raise ValidationError(
                "start_at can't be greater or equal than end_at"
            )
        return attrs

    def create(self, validated_data):
        questions = validated_data.pop("questions")
        task = super().create(validated_data)
        if questions:
            for q in questions:
                q.task = task
            Question.objects.bulk_create(questions)
        return task

    def update(self, instance, validated_data):
        questions = validated_data.pop("questions")
        task = super().update(instance, validated_data)
        if questions:
            current_questions_ids = task.questions.values_list("id", flat=True)

            questions_to_create = []
            questions_to_update = []
            questions_to_delete = []

            for question in questions:
                if not question.id and question.text:
                    question.task = task
                    questions_to_create.append(question)
                elif (
                    question.id
                    and question.text
                    and question.id in current_questions_ids
                ):
                    questions_to_update.append(question)
                elif (
                    question.id
                    and not question.text
                    and question.id in current_questions_ids
                ):
                    questions_to_delete.append(question)

            Question.objects.bulk_create(questions_to_create)
            Question.objects.bulk_update(questions_to_update, fields=("text",))
            Question.objects.filter(
                id__in=[q.id for q in questions_to_delete]
            ).delete()

        return task
