# views.py
from django.shortcuts import render
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from authentication.serializers import (
    LoginUserSerializer,
    LogoutSerializer,
    CreationOfAccountsSerializer,
    AdminUserSerializer,
)
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from . import permissions as custom_permission
from .models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.contrib.sites.shortcuts import get_current_site


class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request):
        try:
            # Validate the incoming data with the serializer
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Authentication is handled within the serializer's validate method,
            # so if it's valid, it's successful, otherwise an exception is raised
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            # Catch validation errors from the serializer and return the error message
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            # Catch authentication failure errors and return a specific message
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Handle unexpected errors and return a generic error message
            return Response(
                {"detail": "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutUserView(generics.GenericAPIView):
    """
    API View for blacklisting the refresh token, effectively logging out the user
    """

    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class CreateAccount(generics.GenericAPIView):
    serializer_class = CreationOfAccountsSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permission.IsSuperAdmin]

    def post(self, request):
        user_type = request.query_params.get("user_type")

        # Validate user_type
        valid_user_types = dict(User.user_choices).keys()
        if not user_type or user_type not in valid_user_types:
            return Response(
                {
                    "detail": f"Invalid user type. Choose from: {', '.join(valid_user_types)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(
            data=request.data, context={"user_type": user_type}
        )

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message": "User account created successfully",
                    "status": status.HTTP_200_OK,
                },
            )
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminListView(generics.ListAPIView):
    """
    API endpoint to list all admin users with pagination
    """

    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permission.IsSuperAdmin]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        # Return all users (admins) except the requesting user
        return User.objects.exclude(id=self.request.user.id).order_by("-created_at")


class AdminDetailView(generics.RetrieveDestroyAPIView):
    """
    API endpoint to retrieve or delete a specific admin user
    """

    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permission.IsSuperAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Prevent deleting yourself
        if instance.id == request.user.id:
            return Response(
                {"detail": "You cannot delete your own account"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(instance)
        return Response(
            {"message": "Admin deleted successfully"}, status=status.HTTP_200_OK
        )


# views.py - Add to your existing views.py file
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from utils import mailer
from .serializers import RequestPasswordResetSerializer, PasswordResetConfirmSerializer
from .models import PasswordResetToken
from authentication.models import User


class RequestPasswordResetView(generics.GenericAPIView):
    """
    API endpoint to request a password reset for admin users
    """

    serializer_class = RequestPasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        frontend_url = request.data.get("frontend_url")
        serializer = self.serializer_class(data={"email": request.data.get("email")})
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)

            # Invalidate any existing tokens for this user
            PasswordResetToken.objects.filter(user=user, is_used=False).update(
                is_used=True
            )

            # Create a new token
            reset_token = PasswordResetToken.objects.create(user=user)

            # Build reset URL (frontend URL)
            reset_url = f"{frontend_url}/reset-password/{reset_token.token}"

            # Send email with reset link
            mailer.sib_send_mail(
                to=[{"email": user.email, "name": user.email}],
                subject="Password Reset Request",
                html_content=f"""
                    <p>Hello,</p>
                    <p>You have requested to reset your password. Please click the link below to reset your password:</p>
                    <p><a href="{reset_url}">Reset Password</a></p>
                    <p>This link will expire in 24 hours.</p>
                    <p>If you did not request this password reset, you can safely ignore this email.</p>
                    <p>Best regards,<br>Admin Team</p>
                """,
            )

        except User.DoesNotExist:
            # We don't want to reveal whether an email exists in our system or not
            pass

        # Always return success response even if email doesn't exist (security best practice)
        return Response(
            {
                "message": "If your email is registered, you will receive password reset instructions."
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmView(generics.GenericAPIView):
    """
    API endpoint to confirm and complete password reset
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_obj = serializer.validated_data["token_obj"]
        user = token_obj.user

        # Update password
        user.set_password(serializer.validated_data["password"])
        user.save()

        # Mark token as used
        token_obj.is_used = True
        token_obj.save()

        # Send confirmation email
        mailer.sib_send_mail(
            to=[{"email": user.email, "name": user.email}],
            subject="Password Reset Successful",
            html_content=f"""
                <p>Hello,</p>
                <p>Your password has been successfully reset.</p>
                <p>If you did not initiate this password reset, please contact our support team immediately.</p>
                <p>Best regards,<br>Admin Team</p>
            """,
        )

        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )


# Admin views for managing password resets (requires authentication)
class AdminPasswordResetView(generics.GenericAPIView):
    """
    API endpoint for superadmins to reset other admin passwords
    """

    permission_classes = [permissions.IsAuthenticated, custom_permission.IsSuperAdmin]

    def post(self, request):
        user_id = request.data.get("user_id")

        try:
            # Ensure the target user exists and is an admin
            user = User.objects.get(id=user_id)

            # Generate temporary password (8 random characters)
            import random
            import string

            temp_password = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )

            # Set the new password
            user.set_password(temp_password)
            user.save()

            # Send email with temporary password
            mailer.sib_send_mail(
                to=[{"email": user.email, "name": user.email}],
                subject="Your Password Has Been Reset",
                html_content=f"""
                    <p>Hello,</p>
                    <p>Your password has been reset by an administrator.</p>
                    <p>Your temporary password is: <strong>{temp_password}</strong></p>
                    <p>Please log in and change your password immediately.</p>
                    <p>Best regards,<br>Admin Team</p>
                """,
            )

            return Response(
                {
                    "message": f"Password reset for {user.email}. Temporary password has been sent."
                },
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
