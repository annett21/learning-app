from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .permissions import IsEmailConfirmed
from .serializers import (ActivateEmailParamsSerializer,
                          ChangePasswordSerializer, RegistrationSerializer,
                          SimpleUserSerializer)
from .tasks import send_email
from .tokens import account_activation_token


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
        Check if user in db or create user and send activation link.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.pop("password")

        user, created = User.objects.get_or_create(
            defaults={"role": User.Role.GUEST},
            **serializer.validated_data,
        )

        if not created and user.is_active:
            return Response(
                data="Account already exists",
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        user.set_password(password)
        user.save()
        send_email.delay(
            subject="Email confirmation",
            message=(
                self.reverse_action("activate-email")
                + f"?uidb64={urlsafe_base64_encode(force_bytes(user.pk))}"
                + f"&token={account_activation_token.make_token(user)}"
            ),
            email=user.email,
        )

        return Response(status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def activate_email(self, request):
        """
        Change email_confirmed db field if id and token validated.
        """
        serializer = ActivateEmailParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        user.email_confirmed = True
        user.save()

        return Response("Thank you for email confirmation!")

    @action(methods=["get"], detail=False, permission_classes=[IsAuthenticated])
    def ping(self, request):
        """
        The crucial view. Do not change this!!!
        """
        return Response("Pong!")

    @action(methods=["post", "get"], detail=False, permission_classes=[IsAuthenticated, IsEmailConfirmed])
    def reset_password(self, request):
        """
        Change password.
        """
        serializer = ChangePasswordSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["password"]
        request.user.set_password(password)
        request.user.save()

        send_email.delay(
            subject="Reset password",
            message=("Password successfully changed, if it wasn't you contact support."),
            email=request.user.email,
        )
        return Response(status=status.HTTP_200_OK)
