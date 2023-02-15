from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    username = models.CharField(max_length=24, unique=True, blank=True)
    password = models.CharField(max_length=16, null=True)
    first_name = models.CharField(max_length=16, blank=True)
    last_name = models.CharField(max_length=16, blank=True)
    email = models.EmailField(unique=True)
    document_number = models.CharField(max_length=16, unique=True)
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    
    def clean(self):
        super().clean()
        if self.is_student == self.is_professor:
            raise ValidationError("User must be a student OR a professor.")
    