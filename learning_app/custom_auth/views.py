from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .permissions import IsEmailConfirmed
from .serializers import (
    ActivateEmailParamsSerializer,
    ChangePasswordSerializer,
    EmailSerializer,
    RegistrationSerializer,
    UserSerializer,
)
from .tasks import send_email
from .tokens import account_activation_token


class UserViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet
):
    """
    A viewset that provides the retrieve, list and update model actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        method="POST",
        request_body=RegistrationSerializer,
        responses={200: ""},
    )
    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
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

    @action(methods=["get"], detail=False, permission_classes=[AllowAny])
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

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def ping(self, request):
        """
        The crucial view. Do not change this!!!
        """
        return Response("Pong!")

    @swagger_auto_schema(
        methods=["post"],
        request_body=ChangePasswordSerializer,
        responses={200: ""},
    )
    @action(
        methods=["post", "get"],
        detail=False,
        permission_classes=[IsAuthenticated, IsEmailConfirmed],
    )
    def reset_password(self, request):
        """
        Change password, if current is valid.
        """
        user = request.user
        serializer = ChangePasswordSerializer(
            data=request.data, context={"user": user}
        )
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["password"]
        user.set_password(password)
        user.save()

        send_email.delay(
            subject="Reset password",
            message=(
                "Password successfully changed, if it wasn't you contact support."
            ),
            email=user.email,
        )
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["post"],
        request_body=EmailSerializer,
        responses={200: ""},
    )
    @action(
        methods=["post", "get"],
        detail=False,
        permission_classes=[IsAuthenticated, IsEmailConfirmed],
    )
    def reset_email(self, request):
        """
        Change current email if it has been confirmed and send confirmation email to a new one.
        """
        user = request.user
        serializer = EmailSerializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user.email = email
        user.email_confirmed = False
        user.save()

        send_email.delay(
            subject="Email confirmation. Email has been changed.",
            message=(
                self.reverse_action("activate-email")
                + f"?uidb64={urlsafe_base64_encode(force_bytes(user.pk))}"
                + f"&token={account_activation_token.make_token(user)}"
            ),
            email=email,
        )

        return Response(status=status.HTTP_200_OK)
