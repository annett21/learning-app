from django.contrib import admin
from .models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ["email", "document_number"]
    list_filter = ["is_student", "is_professor"]

    fieldsets = (
        (
            "Profile",
            {
                "fields": [
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "email",
                    "document_number",
                    "is_student",
                    "is_professor",
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
    readonly_fields = ("password", "date_joined", "username")
