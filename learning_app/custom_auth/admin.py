from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Gives only two options for role choices."""

    role_choices = (
        (User.Role.PROFESSOR, User.Role.PROFESSOR.label),
        (User.Role.STUDENT, User.Role.STUDENT.label),
        (User.Role.GUEST, User.Role.GUEST.label),
    )

    role = forms.ChoiceField(choices=role_choices)

    class Meta:
        model = User
        fields = "__all__"


class RolesListFilter(admin.SimpleListFilter):
    title = _("role")
    parameter_name = "role"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples...
        """
        return (
            (User.Role.PROFESSOR, User.Role.PROFESSOR.label),
            (User.Role.STUDENT, User.Role.STUDENT.label),
            (User.Role.GUEST, User.Role.GUEST.label),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`...
        """
        if self.value() == User.Role.PROFESSOR:
            return queryset.filter(role=User.Role.PROFESSOR)
        if self.value() == User.Role.STUDENT:
            return queryset.filter(role=User.Role.STUDENT)
        if self.value() == User.Role.GUEST:
            return queryset.filter(role=User.Role.GUEST)


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    form = UserChangeForm

    list_display = ("email", "document_number", "role")
    list_filter = (RolesListFilter,)

    fieldsets = (
        (
            "Profile",
            {
                "fields": [
                    "password",
                    "first_name",
                    "last_name",
                    "email",
                    "document_number",
                    "role",
                    "last_login",
                ]
            },
        ),
        (
            "Other",
            {
                "fields": ["date_joined", "is_active"],
            },
        ),
    )
    readonly_fields = ("password", "date_joined")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(role__in=(User.Role.PROFESSOR, User.Role.STUDENT, User.Role.GUEST))
        )


admin.site.unregister(Group)
