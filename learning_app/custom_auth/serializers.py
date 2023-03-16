from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from .models import User
from .tokens import account_activation_token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("role", "email", "first_name", "last_name", "document_number", "email_confirmed")
        read_only_fields = ("role", "email", "email_confirmed")


class PasswordValidationMixin:
    def validate_password(self, password):
        validate_password(password)
        return password
    
    def validate(self, data):
        if data["password"] != data["confirmation_password"]:
            raise serializers.ValidationError({"confirmation_password": "Password fields didn't match."})
        data.pop("confirmation_password")
        return data


class RegistrationSerializer(PasswordValidationMixin, Serializer):
    email = serializers.EmailField()
    document_number = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmation_password = serializers.CharField(max_length=128, write_only=True, required=True)
    
    def validate(self, data):
        data = super().validate(data)
        if User.objects.filter(
            (Q(email=data["email"]) & ~Q(document_number=data["document_number"]))
            | (~Q(email=data["email"]) & Q(document_number=data["document_number"]))
        ).exists():
            raise serializers.ValidationError("Wrong email or document number.")

        return data
    

class ActivateEmailParamsSerializer(Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        uid = force_str(urlsafe_base64_decode(data["uidb64"]))
        user = User.objects.filter(id=uid).first()
        if not user:
            raise serializers.ValidationError({"uidb64": "Unknown user."})
        
        if not account_activation_token.check_token(user, data["token"]):
            raise serializers.ValidationError({"token": "Token expired."})
        
        data["user"] = user

        return data


class ChangePasswordSerializer(PasswordValidationMixin, Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmation_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, old_password):
        if not self.context["user"].check_password(old_password):
            raise serializers.ValidationError("Wrong password.")
        return old_password
    

class EmailSerializer(Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        current_email = self.context["user"].email

        if email == current_email:
            raise serializers.ValidationError("This is already your current email.")

        return email
