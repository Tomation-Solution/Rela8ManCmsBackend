from django.shortcuts import render
from rest_framework import generics, permissions
from news.models import News
from news.serializers import NewsSerializer
from rest_framework.parsers import FormParser
from utils import custom_parsers, custom_response
# Create your views here.


class NewsView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewsSerializer
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser,)

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def get_queryset(self):
        queryset = News.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="news")


class NewsDetialView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser,)
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(writer=self.request.user)


# PUBLIC CLASS HERE
class NewsViewPublic(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="news")
