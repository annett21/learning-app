from rest_framework.permissions import BasePermission


class IsEmailConfirmed(BasePermission):
    message = "Your email haven't been confirmed."

    def has_permission(self, request, view):
        return request.user and request.user.email_confirmed
