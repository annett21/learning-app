from custom_auth.models import User
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=256, unique=True, blank=False)
    professor = models.ForeignKey(User, related_name="profess_courses", blank=False, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name="studied_courses")
    max_students = models.IntegerField(blank=False, default=150)

    def __str__(self):
        return self.title
