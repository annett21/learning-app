from custom_auth.models import User
from django.contrib import admin

from .models import Course


@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ("title", "professor", "max_students")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "professor":
            kwargs["queryset"] = User.objects.filter(role=User.Role.PROFESSOR)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "students":
            kwargs["queryset"] = User.objects.filter(role=User.Role.STUDENT)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
