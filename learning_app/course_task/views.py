from custom_auth.permissions import IsProfessor
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Task
from .serializers import TaskSerializer


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
