from django.shortcuts import render
from rest_framework import generics, status, exceptions, permissions
from rest_framework.parsers import FormParser
from utils import custom_parsers, custom_response, custom_permissions
from aboutus import serializers
from aboutus import models

# Create your views here.


class AboutContactUsView(generics.GenericAPIView):
    serializer_class = serializers.AboutContactUsSerializer
    permission_classes = (custom_permissions.IsPostRequestOrAuthenticated,)

    def get_queryset(self):
        return models.AboutContactUs.objects.all()

    def get(self, request,  id=None):
        contacts = self.get_queryset()
        serializer = self.serializer_class(contacts, many=True)
        return custom_response.Success_response(msg="contacts", data=serializer.data)

    def post(self, request):
        contact_data = request.data
        serializer = self.serializer_class(data=contact_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        contact_data = serializer.data
        return custom_response.Success_response(msg="contact message sent", status_code=status.HTTP_201_CREATED, data=contact_data)


class AboutContactUsDetailsView(generics.GenericAPIView):
    serializer_class = serializers.AboutContactUsSerializer
    permission_classes = (custom_permissions.IsPostRequestOrAuthenticated,)

    def delete(self, request, id=None):
        try:
            contact = models.AboutContactUs.objects.get(id=id)
            contact.delete()
            return custom_response.Success_response(msg="contact deleted")
        except models.AboutContactUs.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


class AboutHistoryView(generics.GenericAPIView):
    serializer_class = serializers.AboutHistorySerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        try:
            about_data = models.AboutHistory.objects.get(id=1)
            serializer = self.serializer_class(about_data)

            return custom_response.Success_response(msg="about history", data=serializer.data)
        except models.AboutHistory.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_data = request.data
        about_data = models.AboutHistory.objects.get(id=1)
        serializer = self.serializer_class(about_data, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="about history updated", data=serializer.data)


class AboutAdvocacyView(generics.GenericAPIView):
    serializer_class = serializers.AboutAdvocacySerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        try:
            about_data = models.AboutAdvocacy.objects.get(id=1)
            serializer = self.serializer_class(about_data)

            return custom_response.Success_response(msg="about advocacy", data=serializer.data)
        except models.AboutAdvocacy.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_data = request.data
        about_data = models.AboutAdvocacy.objects.get(id=1)
        serializer = self.serializer_class(about_data, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="about advocacy updated", data=serializer.data)


class AboutAffilliateView(generics.GenericAPIView):
    serializer_class = serializers.AboutAffilliateSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        try:
            about_data = models.AboutAffilliate.objects.get(id=1)
            serializer = self.serializer_class(about_data)

            return custom_response.Success_response(msg="about affilliate", data=serializer.data)
        except models.AboutAffilliate.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_data = request.data
        about_data = models.AboutAffilliate.objects.get(id=1)
        serializer = self.serializer_class(about_data, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="about affilliate updated", data=serializer.data)


class AboutHowWeWorkView(generics.GenericAPIView):
    serializer_class = serializers.AboutHowWeWorkSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        try:
            about_data = models.AboutHowWeWork.objects.get(id=1)
            serializer = self.serializer_class(about_data)

            return custom_response.Success_response(msg="about how we work", data=serializer.data)
        except models.AboutHowWeWork.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_data = request.data
        about_data = models.AboutHowWeWork.objects.get(id=1)
        serializer = self.serializer_class(about_data, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="about how we work updated", data=serializer.data)


class AboutWhereWeOperatView(generics.GenericAPIView):
    serializer_class = serializers.AboutWhereWeOperateSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        try:
            about_data = models.AboutWhereWeOperate.objects.get(id=1)
            serializer = self.serializer_class(about_data)

            return custom_response.Success_response(msg="about where we operate", data=serializer.data)
        except models.AboutWhereWeOperate.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_data = request.data
        about_data = models.AboutWhereWeOperate.objects.get(id=1)
        serializer = self.serializer_class(about_data, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="about where we operate updated", data=serializer.data)


class AboutWhereWeOperateOfficeViews(generics.ListCreateAPIView):
    serializer_class = serializers.AboutWhereWeOperateOfficeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.AboutWhereWeOperateOffice.objects.all()
        return queryset

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="operation offices")


class AboutWhereWeOperateOfficeDetailViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AboutWhereWeOperateOfficeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return models.AboutWhereWeOperateOffice.objects.all()


class AboutWhereWeOperateBranchViews(generics.ListCreateAPIView):
    serializer_class = serializers.AboutWhereWeOperateBranchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.AboutWhereWeOperateBranch.objects.all()
        return queryset

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="branch offices")


class AboutWhereWeOperateBranchDetailsViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AboutWhereWeOperateBranchSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return models.AboutWhereWeOperateBranch.objects.all()


class AboutOurExecutivesViews(generics.ListCreateAPIView):
    serializer_class = serializers.AboutOurExecutivesSerializer
    permission_classes = [custom_permissions.IsAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get_queryset(self):
        return models.AboutOurExecutives.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializers = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="our executives data", data=serializers.data)


class AboutOurExecutivesDetailViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AboutOurExecutivesSerializer
    permission_classes = [custom_permissions.IsAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]
    lookup_field = "id"

    def get_queryset(self):
        return models.AboutOurExecutives.objects.all()


# PUBLIC VIEW
class AboutWhereWeOperateBranchPublicViews(generics.ListAPIView):
    serializer_class = serializers.AboutWhereWeOperateBranchSerializer

    def get_queryset(self):
        queryset = models.AboutWhereWeOperateBranch.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="branch offices")


class AboutWhereWeOperateOfficePublicViews(generics.ListAPIView):
    serializer_class = serializers.AboutWhereWeOperateOfficeSerializer

    def get_queryset(self):
        queryset = models.AboutWhereWeOperateOffice.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="operation offices")


class AboutOurExecutivesPublicView(generics.ListAPIView):
    serializer_class = serializers.AboutOurExecutivesSerializer

    def get_queryset(self):
        return models.AboutOurExecutives.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="our executives data")
