from django.urls import include, path
from rest_framework import routers

from .views import (
    CourseViewSet,
    ProfessorCoursesViewSet,
    StudentCoursesViewSet,
)

default_router = routers.SimpleRouter()
default_router.register("course", CourseViewSet)

professor_router = routers.SimpleRouter()
professor_router.register("professor/course", ProfessorCoursesViewSet)

student_router = routers.SimpleRouter()
student_router.register("student/course", StudentCoursesViewSet)


urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(professor_router.urls)),
    path("", include(student_router.urls)),
]
