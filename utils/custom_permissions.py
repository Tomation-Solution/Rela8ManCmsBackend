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


class CanAccessPublicationNews(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.user_type in ["publication_news"]


class CanAccessEventTraining(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.user_type in ["event_training"]


class CanAccessPublicView(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.user_type in ["public_view"]


class CanAccessRegistrationPayment(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.user_type in ["registrations_payments"]


class CanAccessProspectiveCertificates(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.user.user_type in ["prospective_certificates"]
