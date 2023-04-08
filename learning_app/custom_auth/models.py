from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_superuser(self, email, password):
        superuser = self.model(
            email=self.normalize_email(email),
            role=User.Role.ADMIN,
            is_active=True,
        )
        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser):
    class Role(models.TextChoices):
        ADMIN = "AD", _("Admin")
        PROFESSOR = "PR", _("Professor")
        STUDENT = "ST", _("Student")
        GUEST = "GU", _("Guest")
        OUT_OF_ROLE = "OOR", _("Out of role")

    role = models.CharField(
        max_length=4,
        choices=Role.choices,
        default=Role.OUT_OF_ROLE,
    )
    password = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=16, blank=True)
    last_name = models.CharField(max_length=16, blank=True)
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    document_number = models.CharField(max_length=16, null=True, unique=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

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
        return self.role == self.Role.ADMIN

    @property
    def is_professor(self):
        return self.role == self.Role.PROFESSOR

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT
