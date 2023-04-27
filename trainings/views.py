from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.parsers import FormParser
from trainings.models import Training
from trainings.serializers import TrainingsSerializer
from utils import custom_response, custom_parsers
# Create your views here.


class TrainingsView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingsSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = Training.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="trainings", data=serializer.data)


class TrainingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingsSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
    lookup_field = "id"

    def get_queryset(self):
        queryset = Training.objects.all()
        return queryset.filter(writer=self.request.user)


class TrainingsViewPublic(generics.ListAPIView):
    serializer_class = TrainingsSerializer

    def get_queryset(self):
        queryset = Training.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="public trainings")
    
