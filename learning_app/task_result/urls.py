from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ProfessorAnswerViewSet, StudentAnswerViewSet

professor_router = SimpleRouter()
professor_router.register("professor/answer", ProfessorAnswerViewSet)

student_router = SimpleRouter()
student_router.register("student/answer", StudentAnswerViewSet)

urlpatterns = [
    path("", include(professor_router.urls)),
    path("", include(student_router.urls)),
]
