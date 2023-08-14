from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, parsers, exceptions
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
            agm_data = models.AGMHomepageCMS.objects.get(pk=1)
            serializer = self.serializer_class(agm_data)

            return custom_response.Success_response(msg="agm homepage content", data=serializer.data)

        except models.AGMHomepageCMS.DoesNotExist:
            raise exceptions.NotFound
        except:
            return custom_response.Failure_response(msg="bad request")

    def patch(self, request):
        data = request.data

        agmcms_data = get_object_or_404(models.AGMHomepageCMS, pk=1)
        serializer = self.serializer_class(
            agmcms_data, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="updated agm homepage", data=serializer.data)


class AGMProgrammeCMSView(generics.GenericAPIView):
    serializer_class = agmcms_serializers.AGMProgrammeCMSSerializer
    parser_classes = [parsers.FormParser, custom_parsers.NestedMultipartParser]
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]

    def get(self, request):
        try:
            agm_data = models.AGMProgrammeCMS.objects.get(pk=1)
            serializer = self.serializer_class(agm_data)

            return custom_response.Success_response(msg="agm programme content", data=serializer.data)

        except models.AGMProgrammeCMS.DoesNotExist:
            raise exceptions.NotFound
        except:
            return custom_response.Failure_response(msg="bad request")

    def patch(self, request):
        data = request.data

        agmcms_data = get_object_or_404(models.AGMProgrammeCMS, pk=1)
        serializer = self.serializer_class(
            agmcms_data, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="updated agm programme", data=serializer.data)


class AGMProgramsView(generics.ListCreateAPIView):
    serializer_class = agmcms_serializers.AGMProgramsSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, custom_parsers.NestedMultipartParser]

    def get_queryset(self):
        return models.AGMPrograms.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="all agm programs", data=serializer.data)


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
        return models.AGMSpeakers.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="all agm speakers", data=serializer.data)


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
            agm_data = models.AGMVenue.objects.get(pk=1)
            serializer = self.serializer_class(agm_data)

            return custom_response.Success_response(msg="agm venue content", data=serializer.data)

        except models.AGMVenue.DoesNotExist:
            raise exceptions.NotFound
        except:
            return custom_response.Failure_response(msg="bad request")

    def patch(self, request):
        data = request.data

        agmcms_data = get_object_or_404(models.AGMVenue, pk=1)
        serializer = self.serializer_class(
            agmcms_data, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="updated agm venue", data=serializer.data)


class AGMExhibitionCMSView(generics.GenericAPIView):
    serializer_class = agmcms_serializers.AGMExhibitionCMSSerializer
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]

    def get(self, request):
        try:
            agm_data = models.AGMExhibitionCMS.objects.get(pk=1)
            serializer = self.serializer_class(agm_data)

            return custom_response.Success_response(msg="agm exhibition content", data=serializer.data)

        except models.AGMExhibitionCMS.DoesNotExist:
            raise exceptions.NotFound
        except:
            return custom_response.Failure_response(msg="bad request")

    def patch(self, request):
        data = request.data

        agmcms_data = get_object_or_404(models.AGMExhibitionCMS, pk=1)
        serializer = self.serializer_class(
            agmcms_data, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="updated agm exhibition", data=serializer.data)


class AGMPreviousExhibitionImagesView(generics.ListCreateAPIView):
    serializer_class = agmcms_serializers.AGMPreviousExhibitionAndCompanyImagesSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get_queryset(self):
        return models.AGMPreviousExhibitionAndCompanyImages.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="all previous exhibition images", data=serializer.data)


class AGMPreviousExhibitionImagesDetailedView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = agmcms_serializers.AGMPreviousExhibitionAndCompanyImagesSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    lookup_field = "id"

    def get_queryset(self):
        return models.AGMPreviousExhibitionAndCompanyImages.objects.all()


class AGMFAQView(generics.ListCreateAPIView):
    serializer_class = agmcms_serializers.AGMFAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.AGMFAQ.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="all agm faqs", data=serializer.data)


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
        return models.AGMPrograms.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="all programs")


class AGMSpeakersPublicView(generics.ListAPIView):
    serializer_class = agmcms_serializers.AGMSpeakersSerializer

    def get_queryset(self):
        return models.AGMSpeakers.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="all speakers")


class AGMPreviousExhibitionImagesPublicView(generics.ListAPIView):
    serializer_class = agmcms_serializers.AGMPreviousExhibitionAndCompanyImagesSerializer

    def get_queryset(self):
        return models.AGMPreviousExhibitionAndCompanyImages.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="all previous exhibition images")


class AGMFAQPublicView(generics.ListAPIView):
    serializer_class = agmcms_serializers.AGMFAQSerializer

    def get_queryset(self):
        return models.AGMFAQ.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="all agm faqs")
