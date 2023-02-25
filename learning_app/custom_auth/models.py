from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_superuser(self, email, password):
        superuser = self.model(email=self.normalize_email(email), role=User.UserRole.ADMIN)
        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser):
    class UserRole(models.TextChoices):
        ADMIN = "AD", _("Admin")
        PROFESSOR = "PR", _("Professor")
        STUDENT = "ST", _("Student")
        OUT_OF_ROLE = "OOR", _("Out of role")

    role = models.CharField(
        max_length=4,
        choices=UserRole.choices,
        default=UserRole.OUT_OF_ROLE,
    )
    password = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=16, blank=True)
    last_name = models.CharField(max_length=16, blank=True)
    email = models.EmailField(unique=True)
    document_number = models.CharField(max_length=16, unique=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def clean(self):
        super().clean()
        if not self.role in {
            self.UserRole.PROFESSOR,
            self.UserRole.STUDENT,
        }:
            raise ValidationError("User must be a student OR a professor.")

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        if self.role == self.UserRole.ADMIN:
            return True



