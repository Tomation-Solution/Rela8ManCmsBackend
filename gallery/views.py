from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser
from utils import custom_parsers, custom_response
from gallery.serializers import GallerySerializer, GalleryRenameSerializer, GalleryItemSerializer
from gallery.models import Gallery, GalleryItems

# Create your views here.


class GalleryView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GallerySerializer

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = Gallery.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="gallery", data=serializer.data)


class GalleryDetailView(generics.RetrieveDestroyAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(writer=self.request.user)


class GalleryRenameView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GalleryRenameSerializer

    def post(self, request, id):
        body = request.data
        serializer = self.serializer_class(data=body)
        if serializer.is_valid(raise_exception=True):
            try:
                gallery = Gallery.objects.get(id=id)
                gallery.name = serializer.data["name"]
                gallery.save()
                return custom_response.Success_response(msg="gallery renamed sucessfully", data=serializer.data)
            except Gallery.DoesNotExist as exc:
                return custom_response.Response(data={"message": "invalid gallery id"}, status=status.HTTP_404_NOT_FOUND)
            except:
                return custom_response.Response(data={"message": "gallery rename failed"}, status=status.HTTP_400_BAD_REQUEST)


class GalleryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GalleryItemSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        gallery = Gallery.objects.get(writer=self.request.user)
        return GalleryItems.objects.filter(gallery=gallery)


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
