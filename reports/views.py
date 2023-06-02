from django.shortcuts import render
from rest_framework import generics, permissions
from reports.models import Reports
from reports.serializers import ReportsSerializer
from rest_framework.parsers import FormParser
from utils import custom_parsers, custom_response
# Create your views here.


class ReportsView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ReportsSerializer
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser,)

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def get_queryset(self):
        queryset = Reports.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="reports")


class ReportsDetialView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser,)
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset


# PUBLIC CLASS HERE
class ReportsViewPublic(generics.ListAPIView):
    serializer_class = ReportsSerializer

    def get_queryset(self):
        queryset = Reports.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="reports")
