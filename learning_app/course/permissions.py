from rest_framework.permissions import BasePermission, SAFE_METHODS

from custom_auth.models import User


class IsCourseModerator(BasePermission):
    message = "You don't have a permission for this action."

    def has_permission(self, request, view):
        if request.user.role == User.Role.STUDENT and request.method not in SAFE_METHODS:
            return False
        else:
            return True
