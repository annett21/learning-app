from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    ProfessorAnswerViewSet,
    ProfessorResultViewSet,
    StudentAnswerViewSet,
    StudentResultViewSet,
)

professor_router = SimpleRouter()
professor_router.register("professor/answer", ProfessorAnswerViewSet)
professor_router.register("professor/result", ProfessorResultViewSet)

student_router = SimpleRouter()
student_router.register("student/answer", StudentAnswerViewSet)
student_router.register("student/result", StudentResultViewSet)

urlpatterns = [
    path("", include(professor_router.urls)),
    path("", include(student_router.urls)),
]
