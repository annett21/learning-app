from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def username_validator(username):
    """
    Check if username is unique if not blank.
    """
    if not username:
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                _(f"{username} should be unique"),
                params={'value': username},
            )


class User(models.Model):
    username = models.CharField(max_length=24, blank=True, validators=[username_validator])
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
    