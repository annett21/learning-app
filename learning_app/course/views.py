from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Course
from .permissions import IsProfessorOrSafeMethod
from .serializers import CourseSerializer


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Returns course object. Any user can get any course."
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Returns a list of all courses."
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
            "Updates a course. `professor` field is read only."
            "Professors can update only own courses."
        )
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description=(
            "Deletes a course. Professors can delete only own courses."
        )
    ),
)
class CourseViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing the courses
    associated with the professor.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsProfessorOrSafeMethod)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.method not in SAFE_METHODS:
            queryset = queryset.filter(professor=self.request.user)

        return queryset
