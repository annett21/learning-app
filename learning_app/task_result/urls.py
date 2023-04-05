from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ProfessorAnswerViewSet

professor_router = SimpleRouter()
professor_router.register("professor/answer", ProfessorAnswerViewSet)

urlpatterns = [path("", include(professor_router.urls))]
