from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from authentication.serializers import LoginUserSerializer, LogoutSerializer
# Create your views here.


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
