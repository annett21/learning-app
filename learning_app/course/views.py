from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from .models import Course
from .permissions import IsProfessorOrSafeMethod
from .serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing the courses
    associated with the professor.

    `Retrieve` request returns course object. Any user can get any course.

    `List` request returns a list of all courses

    `Create` request creates a course and set auth user as professor

    `Update` request updates a course. `professor` field is read only.
    Professors can update only own courses.

    `Delete` request deletes a course. Professors can delete only own courses.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsProfessorOrSafeMethod,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.method not in SAFE_METHODS:
            queryset = queryset.filter(professor=self.request.user)

        return queryset
