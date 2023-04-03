from django.contrib import admin

from .models import Question, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "start_at", "end_at")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ("text", "task__title")
    list_display = ("__str__", "task")
    list_filter = ("task",)
