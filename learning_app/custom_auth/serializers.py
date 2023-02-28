from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RegistrationSerializer(ModelSerializer):
    email = serializers.EmailField()
    document_number = serializers.CharField(max_length=16)

    class Meta:
        model = User
        fields = ["email", "document_number"]
