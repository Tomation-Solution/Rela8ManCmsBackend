from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from trainings.models import Training, TrainingBanner
from trainings.serializers import TrainingsSerializer
from utils import custom_response, custom_parsers
from trainings import serializers

# Create your views here.


from rest_framework.pagination import PageNumberPagination
from datetime import datetime


class PublicTrainingBannerView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            banner = TrainingBanner.objects.first()
            if not banner:
                return Response(
                    {"detail": "No banner found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = serializers.TrainingBannerSerializer(banner)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProtectedTrainingBannerUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        try:
            banner = TrainingBanner.objects.first()
            if not banner:
                banner = TrainingBanner.objects.create()

            serializer = serializers.TrainingBannerSerializer(
                banner, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomTrainingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class TrainingsView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingsSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
    pagination_class = CustomTrainingPagination

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def get_queryset(self):
        queryset = Training.objects.all()
        is_concluded = self.request.query_params.get("is_concluded")

        if is_concluded is not None:
            if is_concluded.lower() == "true":
                queryset = queryset.filter(end_date__lt=datetime.now().date())
            elif is_concluded.lower() == "false":
                queryset = queryset.filter(end_date__gte=datetime.now().date())

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="trainings", data=serializer.data)


# class TrainingsView(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = TrainingsSerializer
#     parser_classes = [custom_parsers.NestedMultipartParser, FormParser]

#     def perform_create(self, serializer):
#         return serializer.save(writer=self.request.user)

#     def list(self, request):
#         queryset = Training.objects.all()
#         serializer = self.serializer_class(queryset, many=True)
#         return custom_response.Success_response(msg="trainings", data=serializer.data)


class TrainingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrainingsSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
    lookup_field = "id"

    def get_queryset(self):
        queryset = Training.objects.all()
        return queryset


class TrainingsViewPublic(generics.ListAPIView):
    serializer_class = TrainingsSerializer

    def get_queryset(self):
        queryset = Training.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="public trainings"
        )
