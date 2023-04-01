from django.db import models
from course.models import Course


class Task(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="tasks"
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
