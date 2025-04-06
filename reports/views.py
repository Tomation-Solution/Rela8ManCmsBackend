from django.shortcuts import render
from rest_framework import generics, permissions, status
from reports.models import Reports
from reports.serializers import ReportsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from utils import custom_parsers, custom_response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class ReportsPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = "page_size"  # Allow clients to override the page size
    max_page_size = 50  # Limit the maximum items per page


class ReportsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = ReportsPagination  # Assign pagination

    def get(self, request):
        reports = Reports.objects.all()
        paginator = self.pagination_class()
        paginated_reports = paginator.paginate_queryset(reports, request)
        serializer = ReportsSerializer(
            paginated_reports, many=True, context={"request": request}
        )

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ReportsSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportsDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, id):
        try:
            return Reports.objects.get(id=id)
        except Reports.DoesNotExist:
            return None

    def get(self, request, id):
        report = self.get_object(id)
        if not report:
            return Response(
                {"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReportsSerializer(report, context={"request": request})
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, id):
        report = self.get_object(id)
        if not report:
            return Response(
                {"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReportsSerializer(
            report, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        report = self.get_object(id)
        if not report:
            return Response(
                {"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND
            )
        report.delete()
        return Response(
            {"message": "Report deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


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
