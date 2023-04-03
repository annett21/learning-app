from django.urls import include, path
from rest_framework import routers

from .views import ProfessorTaskViewSet

professor_router = routers.SimpleRouter()
professor_router.register("professor/task", ProfessorTaskViewSet)

urlpatterns = [path("", include(professor_router.urls))]
