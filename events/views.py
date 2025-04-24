from datetime import datetime
from django.utils import timezone
from rest_framework import generics, permissions, decorators, exceptions, parsers
from rest_framework.parsers import FormParser
from agmcms.models import (
    AGMFAQ,
    AGMExhibitionCMS,
    AGMHomepageCMS,
    AGMPreviousExhibitionAndCompanyImages,
    AGMProgrammeCMS,
    AGMPrograms,
    AGMSpeakers,
    AGMVenue,
)
from events.models import Event
from events.serializers import EventsSerializer
from utils import custom_response, custom_parsers

# Create your views here.


@decorators.api_view(["GET"])
def getAGMEvent(request):
    if request.method == "GET":
        agm_event = Event.objects.get(is_agm=True, is_current_agm=True)
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


# events/views.py


class EventView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
    serializer_class = EventsSerializer
    pagination_class = CustomEventPagination

    def get_queryset(self, request):
        qs = Event.objects.all()
        is_agm = request.query_params.get("is_agm")
        is_current_agm = request.query_params.get("is_current_agm")
        is_concluded = request.query_params.get("is_concluded")

        if is_agm is not None:
            if is_agm.lower() == "true":
                qs = qs.filter(is_agm=True)
                if is_current_agm is not None:
                    if is_current_agm.lower() == "true":
                        qs = qs.filter(is_current_agm=True)

        if is_concluded is not None:
            today = timezone.now().date()
            if is_concluded.lower() == "true":
                qs = qs.filter(end_date__lt=today)
            else:
                qs = qs.filter(end_date__gte=today)
        return qs

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset(request)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request, view=self)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.serializer_class(qs, many=True)
        return custom_response.Success_response(msg="events", data=serializer.data)

    def post(self, request, *args, **kwargs):
        print("➤ Entering EventView.post()")
        data = request.data
        print("  • raw request.data:", data)
        files = request.FILES
        print("  • raw request.FILES:", files)

        # parse flags
        is_agm_flag = str(data.get("is_agm", "")).lower() == "true"
        is_current_agm_flag = str(data.get("is_current_agm", "")).lower() == "true"
        print(
            f"  • Parsed is_agm_flag={is_agm_flag}, is_current_agm_flag={is_current_agm_flag}"
        )

        # enforce single current AGM
        if is_agm_flag and is_current_agm_flag:
            print("  • Enforcing single current AGM: resetting existing ones to False")
            reset_count = Event.objects.filter(is_current_agm=True).update(
                is_current_agm=False
            )
            print(f"    – Updated {reset_count} existing event(s)")

        # validate & save Event
        print("  • Validating serializer with data…")
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            # log the full errors dict
            print("  ✗ Serializer validation failed with errors:", serializer.errors)
            # then raise a DRF ValidationError containing those errors
            raise exceptions.ValidationError(serializer.errors)
        print("  ✓ Serializer is valid")

        try:
            print("  • Saving new Event instance…")
            event = serializer.save(
                writer=request.user,
                is_agm=is_agm_flag,
                is_current_agm=(is_agm_flag and is_current_agm_flag),
            )
            print(f"  ✓ Event saved with id={event.id}")

            # pre-create empty AGM rows if needed
            if is_agm_flag:
                print("  • Pre-creating related AGM CMS rows…")
                print("    – AGMHomepageCMS")
                AGMHomepageCMS.objects.create(event_id=event)
                print("    – AGMProgrammeCMS")
                AGMProgrammeCMS.objects.create(event_id=event)
                print("    – AGMPrograms")
                AGMPrograms.objects.create(event_id=event)
                print("    – AGMSpeakers")
                AGMSpeakers.objects.create(event_id=event)
                print("    – AGMVenue")
                AGMVenue.objects.create(event_id=event)
                print("    – AGMExhibitionCMS")
                AGMExhibitionCMS.objects.create(event_id=event)
                print("    – AGMPreviousExhibitionAndCompanyImages")
                AGMPreviousExhibitionAndCompanyImages.objects.create(event_id=event)
                print("    – AGMFAQ")
                AGMFAQ.objects.create(event_id=event)
                print("  ✓ All AGM rows created")

        except Exception as exc:
            print("  ✗ Exception in EventView.post():", exc)
            raise exceptions.ValidationError({"detail": "Error creating event."})

        # return created object
        print("➤ Preparing response for created Event")
        out_serializer = self.serializer_class(event)
        return custom_response.Success_response(
            msg="event created",
            data=out_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


# class EventView(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = EventsSerializer
#     parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
#     pagination_class = CustomEventPagination

#     def perform_create(self, serializer):
#         print(">>>>>>>>>>>>>>Perform Create>>>>>>>>>>>>>>>>>>>")
#         try:

#             data = self.request.data
#             files = self.request.FILES
#             # interpret text flags safely
#             is_agm_flag = str(data.get("is_agm", "")).lower() == "true"
#             is_current_agm_flag = str(data.get("is_current_agm", "")).lower() == "true"

#             # Enforce single current AGM
#             if is_agm_flag and is_current_agm_flag:
#                 Event.objects.filter(is_current_agm=True).update(is_current_agm=False)

#             # Save the Event itself
#             event = serializer.save(
#                 writer=self.request.user,
#                 is_agm=is_agm_flag,
#                 is_current_agm=(is_agm_flag and is_current_agm_flag),
#             )

#             # If this is an AGM, pre-create all the empty CMS rows
#             if is_agm_flag:
#                 AGMHomepageCMS.objects.create(event=event)
#                 AGMProgrammeCMS.objects.create(event=event)
#                 AGMPrograms.objects.create(event=event)
#                 AGMSpeakers.objects.create(event=event)
#                 AGMVenue.objects.create(event=event)
#                 AGMExhibitionCMS.objects.create(event=event)
#                 AGMPreviousExhibitionAndCompanyImages.objects.create(event=event)
#                 AGMFAQ.objects.create(event=event)
#         except Exception as e:
#             print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#             print(e)
#             raise exceptions.ValidationError("Error creating event.")
#         return event

#     def get_queryset(self):
#         queryset = Event.objects.all()
#         is_concluded = self.request.query_params.get("is_concluded")
#         is_agm = self.request.query_params.get("is_agm")

#         if is_agm is not None:
#             if is_agm.lower() == "true":
#                 queryset = queryset.filter(is_agm=True)
#             # elif is_agm.lower() == "false":
#             #     queryset = queryset.exclude(is_agm=True)

#         if is_concluded is not None:
#             if is_concluded.lower() == "true":
#                 queryset = queryset.filter(end_date__lt=datetime.now().date())
#             elif is_concluded.lower() == "false":
#                 queryset = queryset.filter(end_date__gte=datetime.now().date())

#         return queryset

#     def list(self, request):
#         queryset = self.get_queryset()
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.serializer_class(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.serializer_class(queryset, many=True)
#         return custom_response.Success_response(msg="events", data=serializer.data)


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
