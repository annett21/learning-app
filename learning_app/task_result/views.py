from custom_auth.permissions import IsProfessor
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Answer
from .serializers import ProfessorAnswerSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Returns a list of all answers belonging to "
        "professor's courses. Can be filtered by task_id.",
        manual_parameters=[
            openapi.Parameter(
                "task_id",
                openapi.IN_QUERY,
                description="Filter by task",
                type=openapi.TYPE_INTEGER,
            )
        ],
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Updates a answer. "
        "Can be updated only grade field."
    ),
)
class ProfessorAnswerViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Answer.objects.all().order_by("-id")
    permission_classes = (IsAuthenticated, IsProfessor)
    serializer_class = ProfessorAnswerSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("student__email",)

    def get_queryset(self):
        qs = super().get_queryset()
        allowed_courses = self.request.user.profess_courses.all()
        qs = qs.filter(question__task__course__in=allowed_courses)

        task_id = self.request.query_params.get("task_id")
        if task_id:
            qs = qs.filter(question__task=task_id)

        return qs
