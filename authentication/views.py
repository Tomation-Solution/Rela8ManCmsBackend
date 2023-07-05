from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from authentication.serializers import LoginUserSerializer, LogoutSerializer,CreationOfAccountsSerializer
from . import permissions as custom_permission 

class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsSuperAdmin]


    def post(self, request):
        user_type = request.query_params.get('user_type','executive_secretary')
        serializer = self.serializer_class(data=request.data, context={'user_type':user_type})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK,data={'message':'user account created successfully','status':status.HTTP_200_OK})
