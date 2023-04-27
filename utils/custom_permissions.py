from rest_framework.permissions import BasePermission, IsAuthenticated


class IsPostRequestOrAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        else:
            return bool(request.user and request.user.is_authenticated)


class IsGetRequestOrAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:
            return bool(request.user and request.user.is_authenticated)
