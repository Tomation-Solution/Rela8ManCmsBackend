from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from authentication.serializers import (
    LoginUserSerializer,
    LogoutSerializer,
    CreationOfAccountsSerializer,
)
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from . import permissions as custom_permission


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
    This isn't to be used
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
        user_type = request.query_params.get("user_type", "executive_secretary")
        serializer = self.serializer_class(
            data=request.data, context={"user_type": user_type}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "user account created successfully",
                "status": status.HTTP_200_OK,
            },
        )
