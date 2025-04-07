from django.shortcuts import render
from rest_framework import generics, permissions, status, exceptions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from utils import custom_parsers, custom_response
from gallery.serializers import (
    GallerySerializer,
    GalleryRenameSerializer,
    GalleryItemSerializer,
)
from gallery.models import Gallery, GalleryItems


# Create your views here.
class GalleryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class GalleryView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GallerySerializer
    pagination_class = GalleryPagination

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def get_queryset(self):
        return Gallery.objects.all().order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(
                page, context={"request": request}, many=True
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, context={"request": request}, many=True
        )
        return custom_response.Success_response(msg="gallery", data=serializer.data)


class GalleryDetailView(generics.RetrieveDestroyAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
    pagination_class = GalleryPagination

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        # Get paginated gallery items
        paginator = self.pagination_class()
        gallery_items = GalleryItems.objects.filter(gallery=instance).order_by(
            "-id"
        )  # Order latest first

        paginated_items = paginator.paginate_queryset(gallery_items, request)
        item_serializer = GalleryItemSerializer(
            paginated_items, many=True, context={"request": request}
        )

        return paginator.get_paginated_response(
            {
                "id": instance.id,
                "name": instance.name,
                "created_at": instance.created_at,
                "updated_at": instance.updated_at,
                "gallery_items": item_serializer.data,  # Paginated items
            }
        )


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
                return custom_response.Success_response(
                    msg="gallery renamed sucessfully", data=serializer.data
                )
            except Gallery.DoesNotExist as exc:
                return custom_response.Response(
                    data={"message": "invalid gallery id"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except:
                return custom_response.Response(
                    data={"message": "gallery rename failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class GalleryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GalleryItemSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    parser_classes = (
        custom_parsers.NestedMultipartParser,
        FormParser,
    )
    lookup_field = "id"

    def get_queryset(self):
        return GalleryItems.objects.all()


class GalleryAddGalleryItem(generics.GenericAPIView):
    serializer_class = GalleryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (
        custom_parsers.NestedMultipartParser,
        FormParser,
    )

    def post(self, request):
        body = request.data

        gallery = body.get("gallery", None)
        if gallery == None:
            raise exceptions.ValidationError("gallery field is required")

        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(
            "gallery item added", data=serializer.data
        )


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
