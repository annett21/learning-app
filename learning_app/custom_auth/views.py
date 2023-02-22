from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import RegistrationSerializer, SimpleUserSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """
    A viewset that provides the retrieve and list model actions.
    """

    queryset = User.objects.all()
    serializer_class = SimpleUserSerializer
    permission_classes = (AllowAny,)


    @action(methods=['post'], detail=False,
            url_path='register', url_name='register')
    def register(self, request):
        """
        Sent mail with generated username and password
        just check is user in db
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        get_object_or_404(User, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
