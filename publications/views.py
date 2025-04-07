from rest_framework import generics, status
from publications.models import Publication, PublicationType
from publications.serializers import (
    PublicationSerializer,
    PublicationSerializerPaid,
    PublicationTypeSerializer,
)
from rest_framework.parsers import FormParser, MultiPartParser
from utils import custom_parsers, custom_response
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class PublicationView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomPagination

    def get(self, request):
        queryset = Publication.objects.all()

        # Filter by type if provided
        publication_type = request.query_params.get("type", None)
        if publication_type:
            queryset = queryset.filter(type=publication_type)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PublicationSerializer(
            result_page, many=True, context={"request": request}
        )

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PublicationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, id):
        try:
            return Publication.objects.get(id=id)
        except Publication.DoesNotExist:
            return None

    def get(self, request, id):
        publication = self.get_object(id)
        if not publication:
            return Response(
                {"error": "Publication not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PublicationSerializer(publication, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        publication = self.get_object(id)
        if not publication:
            return Response(
                {"error": "Publication not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PublicationSerializer(
            publication, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        publication = self.get_object(id)
        if not publication:
            return Response(
                {"error": "Publication not found"}, status=status.HTTP_404_NOT_FOUND
            )

        publication.delete()
        return Response(
            {"message": "Publication deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class PublicationTypeView(generics.ListCreateAPIView):
    serializer_class = PublicationTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PublicationType.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="all publication types", data=serializer.data
        )


class PublicationTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PublicationTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return PublicationType.objects.all()


# PUBLIC CLASS HERE


class PublicationViewPublic(generics.ListAPIView):
    serializer_class = PublicationSerializer

    def get_queryset(self):
        queryset = Publication.objects.filter(is_paid=False)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="free publications"
        )


class PublicationViewPaidPublic(generics.ListAPIView):
    serializer_class = PublicationSerializerPaid

    def get_queryset(self):
        queryset = Publication.objects.filter(is_paid=True)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="paid publications"
        )


class PublicationTypePublicView(generics.ListAPIView):
    serializer_class = PublicationTypeSerializer

    def get_queryset(self):
        return PublicationType.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="publication type"
        )
