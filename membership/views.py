from rest_framework import generics, permissions, exceptions, status, parsers
from membership import serializers
from membership.models import (
    JoinStepBanner,
    OurMembersBanner,
    WhyJoinBanner,
    WhyJoinMan,
    JoiningStep,
    FAQs,
    HomePage,
    WhyWeAreUnique,
    OurMembers,
    Advertisement,
)
from rest_framework.parsers import FormParser
from rest_framework.views import APIView
from utils import custom_parsers, custom_response, custom_permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class PublicOurMembersBannerView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            banner = OurMembersBanner.objects.first()
            if not banner:
                return Response(
                    {"detail": "No banner found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = serializers.OurMembersBannerSerializer(banner)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProtectedOurMembersBannerUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        try:
            banner = OurMembersBanner.objects.first()
            if not banner:
                banner = OurMembersBanner.objects.create()

            serializer = serializers.OurMembersBannerSerializer(
                banner, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PublicJoinStepBannerView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            banner = JoinStepBanner.objects.first()
            if not banner:
                return Response(
                    {"detail": "No banner found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = serializers.JoinStepBannerSerializer(banner)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProtectedJoinStepBannerUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        try:
            banner = JoinStepBanner.objects.first()
            if not banner:
                banner = JoinStepBanner.objects.create()

            serializer = serializers.JoinStepBannerSerializer(
                banner, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PublicWhyJoinBannerView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            banner = WhyJoinBanner.objects.first()
            if not banner:
                return Response(
                    {"detail": "No banner found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = serializers.WhyJoinBannerSerializer(banner)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProtectedWhyJoinBannerUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        try:
            banner = WhyJoinBanner.objects.first()
            if not banner:
                banner = WhyJoinBanner.objects.create()

            serializer = serializers.WhyJoinBannerSerializer(
                banner, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WhyJoinManView(generics.ListCreateAPIView):
    serializer_class = serializers.WhyJoinManSerializers
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return WhyJoinMan.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="Why Join MAN Listing", data=serializer.data
        )


class WhyJoinManDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.WhyJoinManSerializers
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = "id"

    def get_queryset(self):
        return WhyJoinMan.objects.all()


class JoiningStepView(generics.ListCreateAPIView):
    serializer_class = serializers.JoiningStepSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return JoiningStep.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="Steps To Join Man", data=serializer.data
        )


class JoiningStepDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.JoiningStepSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = "id"

    def get_queryset(self):
        return JoiningStep.objects.all()


class FAQsPagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_size_query_param = "page_size"  # Allow clients to adjust page size
    max_page_size = 50  # Maximum allowed page size


class FAQsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FAQsPagination

    def get(self, request):
        queryset = FAQs.objects.all().order_by("-id")  # Order by newest first

        # Apply pagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = serializers.FAQsSerializer(
            paginated_queryset, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(
            {"msg": "FAQs Listings", "data": serializer.data}
        )

    def post(self, request):
        serializer = serializers.FAQsSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(
                {"msg": "FAQ created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FAQsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.FAQsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = "id"

    def get_queryset(self):
        return FAQs.objects.all()


class HomePageView(APIView):
    serializer_class = serializers.HomePageSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser)

    def get(self, request):
        try:
            home_data = HomePage.objects.get(id=1)
            serializer = self.serializer_class(home_data, context={"request": request})
            return custom_response.Success_response(
                msg="home main", data=serializer.data
            )
        except HomePage.DoesNotExist:
            raise exceptions.NotFound
        except Exception:
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        try:
            # Try to get existing home data
            home_data, created = HomePage.objects.get_or_create(id=1)
            serializer = self.serializer_class(
                home_data, data=request.data, partial=True, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer.data)
            return custom_response.Success_response(
                msg="home main created" if created else "home main updated",
                data=serializer.data
            )
        except Exception as e:
            print("Error:", e)
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )



class WhyWeAreUniqueView(generics.ListCreateAPIView):
    serializer_class = serializers.WhyWeAreUniqueSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser)

    def get_queryset(self):
        return WhyWeAreUnique.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="why we are unique data", data=serializer.data
        )


class WhyWeAreUniqueDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.WhyWeAreUniqueSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser)
    lookup_field = "id"

    def get_queryset(self):
        return WhyWeAreUnique.objects.all()


class OurMembersView(generics.ListCreateAPIView):
    serializer_class = serializers.OurMembersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OurMembers.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="our members", data=serializer.data)


class OurMembersDetialView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.OurMembersSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OurMembers.objects.all()


class AdvertismentView(generics.ListCreateAPIView):
    serializer_class = serializers.AdvertismentViewSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, custom_parsers.NestedMultipartParser]

    def get_queryset(self):
        return Advertisement.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializers = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="all advertisments", data=serializers.data
        )


class AdvertistmentDetailedView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AdvertismentViewSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, custom_parsers.NestedMultipartParser]
    lookup_field = "id"

    def get_queryset(self):
        return Advertisement.objects.all()


# PUBLIC VIEWS HERE


class WhyJoinManPublicView(generics.ListAPIView):
    serializer_class = serializers.WhyJoinManSerializers

    def get_queryset(self):
        return WhyJoinMan.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="Why Join MAN Listing", data=serializer.data
        )


class JoiningStepPublicView(generics.ListAPIView):
    serializer_class = serializers.JoiningStepSerializer

    def get_queryset(self):
        return JoiningStep.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="Steps To Join Man", data=serializer.data
        )


class FAQsPublicView(generics.ListAPIView):
    serializer_class = serializers.FAQsSerializer

    def get_queryset(self):
        return FAQs.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="FAQs Listing", data=serializer.data
        )


class WhyWeAreUniquePublicView(generics.ListAPIView):
    serializer_class = serializers.WhyWeAreUniqueSerializer

    def get_queryset(self):
        return WhyWeAreUnique.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="why we are unique data", data=serializer.data
        )


class OurMembersPublicView(generics.ListAPIView):
    serializer_class = serializers.OurMembersSerializer

    def get_queryset(self):
        return OurMembers.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="our members", data=serializer.data)


class AdvertisementPublicView(generics.ListAPIView):
    serializer_class = serializers.AdvertismentViewSerializer

    def get_queryset(self):
        return Advertisement.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializers = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="all advertisments", data=serializers.data
        )
