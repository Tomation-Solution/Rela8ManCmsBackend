from datetime import datetime
from rest_framework import generics, permissions, decorators, exceptions, parsers
from rest_framework.parsers import FormParser
from events.models import Event
from events.serializers import EventsSerializer
from utils import custom_response, custom_parsers

# Create your views here.


@decorators.api_view(["GET"])
def getAGMEvent(request):
    if request.method == "GET":
        agm_event = Event.objects.get(is_agm=True)
        serializer = EventsSerializer(agm_event)
        return custom_response.Success_response(msg="agm event", data=serializer.data)
    else:
        raise exceptions.MethodNotAllowed


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import EventAndMediaContent, EventBanner
from .serializers import EventAndMediaContentSerializer


class PublicEventAndMediaContentView(APIView):
    """
    Public GET view to retrieve the first EventAndMediaContent instance.
    """

    def get(self, request):
        content = EventAndMediaContent.objects.first()
        if not content:
            return Response(
                {"detail": "Content not available."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = EventAndMediaContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateEventAndMediaContentView(APIView):
    """
    Protected view to create/update the single EventAndMediaContent instance.
    """

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, custom_parsers.NestedMultipartParser]

    def put(self, request):
        content = EventAndMediaContent.objects.first()
        print(request.data)
        if content:
            serializer = EventAndMediaContentSerializer(content, data=request.data)
        else:
            serializer = EventAndMediaContentSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK if content else status.HTTP_201_CREATED,
            )

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from utils import custom_response, custom_parsers
from events import serializers

# Create your views here.


from rest_framework.pagination import PageNumberPagination
from datetime import datetime


class PublicEventBannerView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            banner = EventBanner.objects.first()
            if not banner:
                return Response(
                    {"detail": "No banner found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = serializers.EventBannerSerializer(banner)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProtectedEventBannerUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        try:
            banner = EventBanner.objects.first()
            if not banner:
                banner = EventBanner.objects.create()

            serializer = serializers.EventBannerSerializer(
                banner, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomEventPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class EventView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventsSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
    pagination_class = CustomEventPagination

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def get_queryset(self):
        queryset = Event.objects.all()
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
        return custom_response.Success_response(msg="events", data=serializer.data)


# class EventView(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = EventsSerializer
#     parser_classes = [custom_parsers.NestedMultipartParser, FormParser]

#     def perform_create(self, serializer):
#         return serializer.save(writer=self.request.user)

#     def list(self, request):
#         queryset = Event.objects.all()
#         serializer = self.serializer_class(queryset, many=True)
#         return custom_response.Success_response(msg="events", data=serializer.data)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventsSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
    lookup_field = "id"

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset


class EventViewPublic(generics.ListAPIView):
    serializer_class = EventsSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="events")
