from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics, permissions, status
from news.models import News
from news.serializers import (
    NewsSerializer,
    UploadedImageSerializer,
    NewsUpdateSerializer,
)
from utils import custom_parsers, custom_response


# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 10  # Set default page size
    page_size_query_param = "page_size"  # Allow dynamic page size in query params
    max_page_size = 50  # Set max limit to prevent large responses


class NewsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser)
    pagination_class = CustomPagination  # Add pagination class

    def get(self, request):
        queryset = News.objects.all().order_by("-updated_at")  # Order by latest news
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = NewsSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(
            serializer.data
        )  # Return paginated response

    def post(self, request):
        serializer = NewsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(
                {"message": "News created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Supports file uploads

    def get(self, request, id, *args, **kwargs):
        """
        Retrieve a news item by ID.
        """
        try:
            news = News.objects.get(id=id)
            serializer = NewsSerializer(news, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except News.DoesNotExist:
            return Response(
                {"error": "News not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, id, *args, **kwargs):
        """
        Fully update a news item.
        """
        try:
            news = News.objects.get(id=id)
        except News.DoesNotExist:
            return Response(
                {"error": "News not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = NewsSerializer(
            news, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        """
        Partially update a news item.
        """
        try:
            news = News.objects.get(id=id)
        except News.DoesNotExist:
            return Response(
                {"error": "News not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = NewsUpdateSerializer(
            news, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        """
        Delete a news item.
        """
        try:
            news = News.objects.get(id=id)
            news.delete()
            return Response(
                {"message": "News deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except News.DoesNotExist:
            return Response(
                {"error": "News not found"}, status=status.HTTP_404_NOT_FOUND
            )


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


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print({"url": serializer.data["image"]})
            return Response(
                {
                    "url": request.build_absolute_uri(serializer.data["image"])
                },  # Returns image URL
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
