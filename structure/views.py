from django.shortcuts import render
from rest_framework import generics, permissions, parsers, exceptions, status
from structure.models import SectoralGroup, MRC, MRCServices, MPDCL, MPDCLServices
from structure.serializers import (
    SectoralGroupSerializer,
    MRCSerializer,
    MRCServicesSerializer,
    MPDCLSerializer,
    MPDCLServicesSerializer,
)
from utils import custom_response, custom_parsers, custom_permissions
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import MrcContactPage, SectorialBanner
from .serializers import MrcContactPageSerializer, SectorialBannerSerializer

# Create your views here.

# paginations.py or any utils file


class PublicSectorialBannerView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            banner = SectorialBanner.objects.first()
            if not banner:
                return Response(
                    {"detail": "No banner found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = SectorialBannerSerializer(banner)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProtectedSectorialBannerUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        try:
            banner = SectorialBanner.objects.first()
            if not banner:
                banner = SectorialBanner.objects.create()

            serializer = SectorialBannerSerializer(
                banner, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MrcContactPageView(APIView):
    """
    View for getting and updating the MRC Contact Page.
    GET is public; PATCH requires authentication.
    """

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        """
        Public GET request to retrieve the MRC Contact Page.
        """
        mrc_contact_page = MrcContactPage.objects.first()
        if mrc_contact_page:
            serializer = MrcContactPageSerializer(mrc_contact_page)
            return Response(serializer.data)
        return Response(
            {"message": "MRC Contact Page not found."}, status=status.HTTP_404_NOT_FOUND
        )

    def patch(self, request):
        """
        Protected PATCH request to update or create the MRC Contact Page.
        """
        mrc_contact_page, _ = MrcContactPage.objects.get_or_create(id=1)
        serializer = MrcContactPageSerializer(
            mrc_contact_page, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_size_query_param = (
        "page_size"  # Allow the client to override using ?page_size=
    )
    max_page_size = 100


class SectoralGroupView(generics.ListCreateAPIView):
    serializer_class = SectoralGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    pagination_class = CustomPageNumberPagination  # Add pagination here

    def get_queryset(self):
        return SectoralGroup.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return custom_response.Success_response(
            msg="sectoral groups", data=serializer.data
        )


# class SectoralGroupView(generics.ListCreateAPIView):
#     serializer_class = SectoralGroupSerializer
#     permission_classes = [
#         permissions.IsAuthenticated,
#     ]
#     parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

#     def get_queryset(self):
#         return SectoralGroup.objects.all()

#     def perform_create(self, serializer):
#         return serializer.save(writer=self.request.user)

#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)
#         return custom_response.Success_response(
#             msg="sectoral groups", data=serializer.data
#         )


class SectoralGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SectoralGroupSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    lookup_field = "id"

    def get_queryset(self):
        return SectoralGroup.objects.all()


class MRCView(generics.GenericAPIView):
    serializer_class = MRCSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get(self, request):
        try:
            mrc_data = MRC.objects.get(id=1)
            serializer = self.serializer_class(mrc_data)

            return custom_response.Success_response(
                msg="mrc data", data=serializer.data
            )
        except MRC.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request):
        try:
            update_data = request.data
            print(update_data)
            mrc_data = MRC.objects.get(id=1)
            serializer = self.serializer_class(
                mrc_data, data=update_data, partial=True
            )  # 👈 partial=True
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return custom_response.Success_response(
                msg="mrc data", data=serializer.data
            )
        except Exception as e:
            print(e)
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )


class MRCServicesView(generics.ListCreateAPIView):
    serializer_class = MRCServicesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MRCServices.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="mrc services", data=serializer.data
        )


class MRCServicesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MRCServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return MRCServices.objects.all()


class MPDCLView(generics.GenericAPIView):
    serializer_class = MPDCLSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get(self, request):
        try:
            mpdcl_data = MPDCL.objects.get(id=1)
            serializer = self.serializer_class(mpdcl_data)

            return custom_response.Success_response(
                msg="mpdcl data", data=serializer.data
            )
        except MPDCL.DoesNotExist as exp:
            raise exceptions.NotFound
        except Exception as e:
            print(e)
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request):
        try:
            update_data = request.data
            print(update_data)
            mpdcl_data = MPDCL.objects.get(id=1)
            serializer = self.serializer_class(
                mpdcl_data, data=update_data, partial=True
            )  # 👈 partial=True
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return custom_response.Success_response(
                msg="mpdcl data", data=serializer.data
            )
        except Exception as e:
            print(e)
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )


class MPDCLServicesView(generics.ListCreateAPIView):
    serializer_class = MPDCLServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get_queryset(self):
        return MPDCLServices.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="mpdcl service", data=serializer.data
        )


class MPDCLServicesDetialView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MPDCLServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    lookup_field = "id"

    def get_queryset(self):
        return MPDCLServices.objects.all()


# PUBLIC VIEWS


class SectoralGroupPublicView(generics.ListAPIView):
    serializer_class = SectoralGroupSerializer

    def get_queryset(self):
        return SectoralGroup.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="sectoral groups", data=serializer.data
        )


class MRCServicePublicView(generics.ListAPIView):
    serializer_class = MRCServicesSerializer

    def get_queryset(self):
        return MRCServices.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="mrc service", data=serializer.data)


class MPDCLServicesPublicView(generics.ListAPIView):
    serializer_class = MPDCLServicesSerializer

    def get_queryset(self):
        return MPDCLServices.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="mpdcl service", data=serializer.data
        )
