from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, parsers, exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from agmcms import serializers as agmcms_serializers
from agmcms import models

from utils import custom_permissions, custom_response
from utils import custom_parsers


class AGMHomepageCMSView(generics.GenericAPIView):
    serializer_class = agmcms_serializers.AGMHomepageCMSSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get(self, request):
        try:
            event_id = int(request.query_params.get("id", 1))
            agm_data = models.AGMHomepageCMS.objects.get(event_id=event_id)
            serializer = self.serializer_class(agm_data)

            return custom_response.Success_response(
                msg="agm homepage content", data=serializer.data
            )

        except models.AGMHomepageCMS.DoesNotExist:
            raise exceptions.NotFound
        except:
            return custom_response.Failure_response(msg="bad request")

    def patch(self, request):
        data = request.data

        event_id = int(request.query_params.get("id", 1))
        agmcms_data = get_object_or_404(models.AGMHomepageCMS, event_id=event_id)
        serializer = self.serializer_class(agmcms_data, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(
            msg="updated agm homepage", data=serializer.data
        )


class AGMProgrammeCMSView(generics.GenericAPIView):
    serializer_class = agmcms_serializers.AGMProgrammeCMSSerializer
    parser_classes = [parsers.FormParser, custom_parsers.NestedMultipartParser]
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]

    def get(self, request):
        try:
            event_id = int(request.query_params.get("id", 1))
            agm_data = models.AGMProgrammeCMS.objects.get(event_id=event_id)
            serializer = self.serializer_class(agm_data)

            return custom_response.Success_response(
                msg="agm programme content", data=serializer.data
            )

        except models.AGMProgrammeCMS.DoesNotExist:
            raise exceptions.NotFound
        except:
            return custom_response.Failure_response(msg="bad request")

    def patch(self, request):
        data = request.data

        event_id = int(request.query_params.get("id", 1))
        agmcms_data = get_object_or_404(models.AGMProgrammeCMS, event_id=event_id)
        serializer = self.serializer_class(agmcms_data, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(
            msg="updated agm programme", data=serializer.data
        )


class AGMProgramsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, custom_parsers.NestedMultipartParser]

    def get_queryset(self, request):
        event_id = int(request.query_params.get("id", 1))
        return models.AGMPrograms.objects.filter(event_id=event_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)
        serializer = agmcms_serializers.AGMProgramsSerializer(queryset, many=True)
        return custom_response.Success_response(
            msg="all agm programs", data=serializer.data
        )

    def post(self, request, *args, **kwargs):
        serializer = agmcms_serializers.AGMProgramsSerializer(data=request.data)
        if serializer.is_valid():
            print(request.query_params.get("id", 1))
            serializer.save()
            return custom_response.Success_response(
                msg="AGM program created",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AGMProgramsView(generics.ListCreateAPIView):
#     serializer_class = agmcms_serializers.AGMProgramsSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [parsers.FormParser, custom_parsers.NestedMultipartParser]

#     def perform_create(self, serializer):
#         print(self.request.query_params.get("id", 1))
#         return super().perform_create(serializer)

#     def get_queryset(self):
#         event_id = int(self.request.query_params.get("id", 1))
#         return models.AGMPrograms.objects.filter(event_id=event_id)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)
#         return custom_response.Success_response(
#             msg="all agm programs", data=serializer.data
#         )


class AGMProgramsDetialedView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = agmcms_serializers.AGMProgramsSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, custom_parsers.NestedMultipartParser]
    lookup_field = "id"

    def get_queryset(self):
        return models.AGMPrograms.objects.all()


class AGMSpeakersView(generics.ListCreateAPIView):
    serializer_class = agmcms_serializers.AGMSpeakersSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get_queryset(self):
        event_id = int(self.request.query_params.get("id", 1))
        return models.AGMSpeakers.objects.filter(event_id=event_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="all agm speakers", data=serializer.data
        )


class AGMSpeakersDetialedView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = agmcms_serializers.AGMSpeakersSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    lookup_field = "id"

    def get_queryset(self):
        return models.AGMSpeakers.objects.all()


class AGMVenueView(generics.GenericAPIView):
    serializer_class = agmcms_serializers.AGMVenueSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get(self, request):
        try:
            event_id = int(request.query_params.get("id", 1))
            agm_data = models.AGMVenue.objects.get(event_id=event_id)
            serializer = self.serializer_class(agm_data)

            return custom_response.Success_response(
                msg="agm venue content", data=serializer.data
            )

        except models.AGMVenue.DoesNotExist:
            raise exceptions.NotFound
        except:
            return custom_response.Failure_response(msg="bad request")

    def patch(self, request):
        data = request.data

        event_id = int(request.query_params.get("id", 1))
        agmcms_data = get_object_or_404(models.AGMVenue, event_id=event_id)
        serializer = self.serializer_class(agmcms_data, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(
            msg="updated agm venue", data=serializer.data
        )


class AGMExhibitionCMSView(generics.GenericAPIView):
    serializer_class = agmcms_serializers.AGMExhibitionCMSSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]

    def get(self, request):
        try:
            event_id = int(request.query_params.get("id", 1))
            agm_data = models.AGMExhibitionCMS.objects.get(event_id=event_id)
            serializer = self.serializer_class(agm_data)

            return custom_response.Success_response(
                msg="agm exhibition content", data=serializer.data
            )

        except models.AGMExhibitionCMS.DoesNotExist:
            raise exceptions.NotFound
        except:
            return custom_response.Failure_response(msg="bad request")

    def patch(self, request):
        data = request.data

        event_id = int(request.query_params.get("id", 1))
        agmcms_data = get_object_or_404(models.AGMExhibitionCMS, event_id=event_id)
        serializer = self.serializer_class(agmcms_data, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(
            msg="updated agm exhibition", data=serializer.data
        )


class AGMPreviousExhibitionImagesView(generics.ListCreateAPIView):
    serializer_class = (
        agmcms_serializers.AGMPreviousExhibitionAndCompanyImagesSerializer
    )
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get_queryset(self):
        event_id = int(self.request.query_params.get("id", 1))
        return models.AGMPreviousExhibitionAndCompanyImages.objects.filter(
            event_id=event_id
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            msg="all previous exhibition images", data=serializer.data
        )


class AGMPreviousExhibitionImagesDetailedView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = (
        agmcms_serializers.AGMPreviousExhibitionAndCompanyImagesSerializer
    )
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    lookup_field = "id"

    def get_queryset(self):
        return models.AGMPreviousExhibitionAndCompanyImages.objects.all()


class AGMFAQView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        event_id = int(request.query_params.get("id", 1))
        queryset = models.AGMFAQ.objects.filter(event_id=event_id)
        serializer = agmcms_serializers.AGMFAQSerializer(queryset, many=True)
        return custom_response.Success_response(
            msg="all agm faqs", data=serializer.data
        )

    def post(self, request, *args, **kwargs):
        print("Incoming POST data:", request.data)

        serializer = agmcms_serializers.AGMFAQSerializer(data=request.data)

        print("Serializer instance created.")
        if serializer.is_valid():
            print("Serializer is valid. Saving data...")
            serializer.save()
            print("Data saved successfully.")
            return custom_response.Success_response(
                msg="AGM FAQ created successfully", data=serializer.data
            )
        else:
            print("Serializer is not valid. Errors:")
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AGMFAQView(generics.ListCreateAPIView):
#     serializer_class = agmcms_serializers.AGMFAQSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         event_id = int(self.request.query_params.get("id", 1))
#         return models.AGMFAQ.objects.filter(event_id=event_id)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)
#         return custom_response.Success_response(
#             msg="all agm faqs", data=serializer.data
#         )


class AGMFAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = agmcms_serializers.AGMFAQSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return models.AGMFAQ.objects.all()


# PUBLIC VIEWS


class AGMProgramsPublicView(generics.ListAPIView):
    serializer_class = agmcms_serializers.AGMProgramsSerializer

    def get_queryset(self):
        event_id = int(self.request.query_params.get("id", 0))
        if event_id == 0:
            event_id = models.Event.objects.filter(is_current_agm=True).first().id
        return models.AGMPrograms.objects.filter(event_id=event_id)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="all programs"
        )


class AGMSpeakersPublicView(generics.ListAPIView):
    serializer_class = agmcms_serializers.AGMSpeakersSerializer

    def get_queryset(self):
        event_id = int(self.request.query_params.get("id", 0))
        if event_id == 0:
            event_id = models.Event.objects.filter(is_current_agm=True).first().id
        return models.AGMSpeakers.objects.filter(event_id=event_id)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="all speakers"
        )


class AGMPreviousExhibitionImagesPublicView(generics.ListAPIView):
    serializer_class = (
        agmcms_serializers.AGMPreviousExhibitionAndCompanyImagesSerializer
    )

    def get_queryset(self):
        event_id = int(self.request.query_params.get("id", 0))
        if event_id == 0:
            event_id = models.Event.objects.filter(is_current_agm=True).first().id
        return models.AGMPreviousExhibitionAndCompanyImages.objects.filter(
            event_id=event_id
        )

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="all previous exhibition images"
        )


class AGMFAQPublicView(generics.ListAPIView):
    serializer_class = agmcms_serializers.AGMFAQSerializer

    def get_queryset(self):
        event_id = int(self.request.query_params.get("id", 0))
        if event_id == 0:
            event_id = models.Event.objects.filter(is_current_agm=True).first().id
        return models.AGMFAQ.objects.filter(event_id=event_id)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="all agm faqs"
        )
