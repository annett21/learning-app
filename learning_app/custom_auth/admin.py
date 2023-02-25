from django.contrib import admin

from .models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ("email", "document_number")
    list_filter = ("role",)

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
