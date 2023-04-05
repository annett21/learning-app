from course_task.models import Question
from custom_auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models


def student_directory_path(instance, filename):
    """file will be uploaded to MEDIA_ROOT/answers/student_<id>/<filename>"""
    return f"answers/student_{instance.student.id}/{filename}"


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.TextField(blank=True, null=True)
    attachment = models.FileField(
        upload_to=student_directory_path, blank=True, null=True
    )
    grade = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=(MaxValueValidator(100),)
    )

    def __str__(self):
        return f"Answer ({self.id})"

    def clean(self):
        super().clean()

        if self.question.task.course not in self.student.studied_courses.all():
            err = "The question doesn't belong to user's courses."
            raise ValidationError(err)

        if not self.text and not self.attachment:
            raise ValidationError("Text or attachment is required.")
