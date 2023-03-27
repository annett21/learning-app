from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Course

from rest_framework.views import APIView

from rest_framework.viewsets import ViewSet, ModelViewSet
from .serializers import CourseSerializer

from .permissions import IsCourseModerator




class CourseViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing the courses
    associated with the professor.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsCourseModerator,)
