from custom_auth.models import User
from django.contrib import admin

from .models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "student",
        "question",
        "question_task",
        "question_task_course",
        "grade",
    )
    search_fields = (
        "student__email",
        "question__text",
        "question__task__title",
        "question__task__course__title",
    )

    @admin.display(description="Task", ordering="question__task")
    def question_task(self, obj):
        return str(obj.question.task)

    @admin.display(description="Course", ordering="question__task__course")
    def question_task_course(self, obj):
        return str(obj.question.task.course)

    def get_readonly_fields(self, request, obj):
        read_only_fields = list(super().get_readonly_fields(request, obj))
        if obj:
            read_only_fields.append("student")
        return tuple(read_only_fields)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(role=User.Role.STUDENT)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
