from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.parsers import FormParser
from utils import custom_parsers, custom_response
from gallery.serializers import GallerySerializer
from gallery.models import Gallery

# Create your views here.


class GalleryView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser,)
    serializer_class = GallerySerializer

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = Gallery.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="gallery", data=serializer.data)


class GalleryDetailView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser,)
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(writer=self.request.user)


# PUBLIC CLASS HERE
class GalleryViewPublic(generics.ListAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        queryset = Gallery.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="gallery")


class ReturnBack(generics.GenericAPIView):
    def post(self, request):
        return custom_response.Success_response(msg="working", data=request.data)
