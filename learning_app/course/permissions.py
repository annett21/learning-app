from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProfessorOrSafeMethod(BasePermission):
    message = "You don't have a permission for this action."

    def has_permission(self, request, view):
        if request.user.is_professor:
            return True
        elif request.method in SAFE_METHODS:
            return True
        else:
            return False
