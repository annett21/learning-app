from custom_auth.permissions import IsProfessor, IsStudent
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Answer
from .serializers import (
    ProfessorAnswerSerializer,
    StudentAnswerSerializer,
    StudentAnswerUpdateSerializer,
)


class BaseAnswerViewSet(GenericViewSet):
    queryset = Answer.objects.all().order_by("-id")

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(question__task__course__in=self.allowed_courses)

        task_id = self.request.query_params.get("task_id")
        if task_id:
            qs = qs.filter(question__task=task_id)

        return qs


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
    BaseAnswerViewSet,
):
    queryset = Answer.objects.all().order_by("-id")
    permission_classes = (IsAuthenticated, IsProfessor)
    serializer_class = ProfessorAnswerSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("student__email",)

    @property
    def allowed_courses(self):
        return self.request.user.profess_courses.all()


class StudentAnswerViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    BaseAnswerViewSet,
):
    queryset = Answer.objects.all().order_by("-id")
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_classes = {
        "default": StudentAnswerSerializer,
        "update": StudentAnswerUpdateSerializer,
        "partial_update": StudentAnswerUpdateSerializer,
    }

    def get_serializer_class(self):
        return (
            self.serializer_classes.get(self.action)
            or self.serializer_classes["default"]
        )

    @property
    def allowed_courses(self):
        return self.request.user.studied_courses.all()

    @action(methods=("post",), detail=True)
    def upload_attachment(self, request, pk=None):
        answer = get_object_or_404(self.get_queryset(), pk=pk)
        answer.attachment = request.FILES.get("attachment")
        answer.save()
        return Response(status=status.HTTP_200_OK)