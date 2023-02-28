from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import RegistrationSerializer, SimpleUserSerializer
from .utils import create_password, create_username


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """
    A viewset that provides the retrieve and list model actions.
    """

    queryset = User.objects.all()
    serializer_class = SimpleUserSerializer
    permission_classes = (AllowAny,)

    @action(methods=["post"], detail=False)
    def register(self, request):
        """
        Sending email with temporary username and password if user in db.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, **serializer.validated_data)
        password = create_password()
        username = create_username(user.email)
        send_mail(
            subject="Credentials for registration",
            message=f"Here is your temporary password {password} and username {username}. Tap link to change.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return Response(status=status.HTTP_200_OK)
