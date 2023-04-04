from django.urls import include, path
from rest_framework import routers

from .views import ProfessorTaskViewSet, StudentTaskViewSet

professor_router = routers.SimpleRouter()
professor_router.register("professor/task", ProfessorTaskViewSet)

student_router = routers.SimpleRouter()
student_router.register("student/task", StudentTaskViewSet)

urlpatterns = [
    path("", include(professor_router.urls)),
    path("", include(student_router.urls)),
]
