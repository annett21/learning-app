from django.db.models import Q
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from rest_framework.serializers import ModelSerializer, Serializer

from .models import User
from .tokens import account_activation_token


class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RegistrationSerializer(Serializer):
    email = serializers.EmailField()
    document_number = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmation_password = serializers.CharField(max_length=128, write_only=True, required=True)

    class Meta:
        fields = ["email", "document_number", "password", "confirmation_password"]

    def validate(self, data):
        if data["password"] != data["confirmation_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        data.pop("confirmation_password")
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
