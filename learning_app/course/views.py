from custom_auth.permissions import IsEmailConfirmed, IsProfessor, IsStudent
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Course
from .serializers import CourseSerializer


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Returns a course object. Any user can get any course."
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Returns a list of all courses."
    ),
)
class CourseViewSet(ReadOnlyModelViewSet):
    """A simple ViewSet for viewing courses."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ("title", "professor__first_name", "professor__last_name")


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Returns a course of current professor."
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Returns a list courses of current professor."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Creates a course and set auth user as professor."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description=(
            "Updates a course of current professor. `professor` field is read only."
        )
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Deletes a course of current professor."
    ),
)
class ProfessorCourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by("-id")
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsProfessor)
    filter_backends = (SearchFilter,)
    search_fields = ("title",)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Course.objects.none()

        return super().get_queryset().filter(professor=self.request.user)


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Returns a course of current student."
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Returns a list courses of current student."
    ),
)
class StudentCourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all().order_by("-id")
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsStudent)
    filter_backends = (SearchFilter,)
    search_fields = ("title", "professor__first_name", "professor__last_name")

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Course.objects.none()

        return super().get_queryset().filter(students=self.request.user)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=(IsAuthenticated, IsStudent, IsEmailConfirmed),
    )
    def join_course(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        course.students.add(request.user)
        return Response(status=status.HTTP_200_OK)
