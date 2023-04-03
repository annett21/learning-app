from course.models import Course
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def datetime_gt_now(value):
    if value < timezone.now():
        raise ValidationError("Can't be less than now")


class Task(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="tasks"
    )
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(
        blank=True, null=True, validators=(datetime_gt_now,)
    )

    class Meta:
        unique_together = ("title", "course")

    def __str__(self):
        return f"{self.id} - {self.title}"

    def clean(self):
        super().clean()
        if self.start_at >= self.end_at:
            raise ValidationError(
                "'Start at' field can't be greater than 'End at' field"
            )


class Question(models.Model):
    text = models.TextField(blank=False, null=False)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="questions"
    )

    def __str__(self):
        return f"{self.id} - {self.text[:20]}"
