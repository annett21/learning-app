from rest_framework.permissions import BasePermission


class IsEmailConfirmed(BasePermission):
    message = "Your email haven't been confirmed."

    def has_permission(self, request, view):
        return request.user and request.user.email_confirmed


class IsProfessor(BasePermission):
    message = "Only professors have a permission for this action."

    def has_permission(self, request, view):
        return request.user.is_professor


class IsStudent(BasePermission):
    message = "Only students have a permission for this action."

    def has_permission(self, request, view):
        return request.user.is_student
