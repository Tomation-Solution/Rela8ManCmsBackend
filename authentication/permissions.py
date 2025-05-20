# permissions.py
from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow super_user to access a view
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "super_user"
