from django.contrib.auth.models import BaseUserManager


def create_password():
    password_generator = BaseUserManager().make_random_password
    password = password_generator(length=14)
    return password


def create_username(email):
    username = email.split("@")[0]
    return username
