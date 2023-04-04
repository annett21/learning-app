from custom_auth.permissions import IsProfessor, IsStudent
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Task
from .serializers import TaskSerializer


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Returns a taks belonging to professor's courses. "
        "Can be filtered by course_id."
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Returns a list tasks belonging to professor's courses. "
        "Can be filtered by course_id."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Creates a task with questions."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description=(
            "Updates a task. "
            "Pass question text to create the question. "
            "Pass question id and text to update the question. "
            "Pass only question id to delete the question."
        )
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description=(
            "Updates a task. "
            "Pass question text to create the question. "
            "Pass question id and text to update the question. "
            "Pass only question id to delete the question."
        )
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Deletes a task."),
)
class ProfessorTaskViewSet(ModelViewSet):
    queryset = Task.objects.all().order_by("-id")
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsProfessor)

    def get_queryset(self):
        qs = super().get_queryset().filter(course__professor=self.request.user)
        course_id = self.request.query_params.get("course_id")
        if course_id:
            qs = qs.filter(course=course_id)
        return qs


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Returns a taks belonging to student's courses. "
        "Can be filtered by course_id."
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Returns a list tasks belonging to students's courses. "
        "Can be filtered by course_id."
    ),
)
class StudentTaskViewSet(ReadOnlyModelViewSet):
    queryset = Task.objects.all().order_by("-id")
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def get_queryset(self):
        qs = super().get_queryset().filter(course__students=self.request.user)
        course_id = self.request.query_params.get("course_id")
        if course_id:
            qs = qs.filter(course=course_id)
        return qs
