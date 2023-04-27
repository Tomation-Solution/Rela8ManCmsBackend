from django.shortcuts import render
from rest_framework import generics, permissions, parsers, exceptions, status
from structure.models import SectoralGroup, MRC, MRCServices, MPDCL
from structure.serializers import SectoralGroupSerializer, MRCSerializer, MRCServicesSerializer, MPDCLSerializer
from utils import custom_response, custom_parsers, custom_permissions

# Create your views here.
class SectoralGroupView(generics.ListCreateAPIView):
    serializer_class = SectoralGroupSerializer
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get_queryset(self):
        return SectoralGroup.objects.all()
    
    def perform_create(self, serializer):
        return serializer.save(writer = self.request.user)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="sectoral groups", data=serializer.data)

class SectoralGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SectoralGroupSerializer
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    lookup_field = "id"

    def get_queryset(self):
        return SectoralGroup.objects.filter(writer = self.request.user)
    
class MRCView(generics.GenericAPIView):
    serializer_class = MRCSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]

    def get(self, request):
        try:
            mrc_data = MRC.objects.get(id=1)
            serializer = self.serializer_class(mrc_data)

            return custom_response.Success_response(msg="mrc data", data=serializer.data)
        except MRC.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_data = request.data
        mrc_data = MRC.objects.get(id=1)
        serializer = self.serializer_class(mrc_data, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="mrc data", data=serializer.data)

class MRCServicesView(generics.ListCreateAPIView):
    serializer_class = MRCServicesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MRCServices.objects.all()
    
    def perform_create(self, serializer):
        return serializer.save(writer = self.request.user)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="mrc services", data=serializer.data)
    
class MRCServicesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MRCServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return MRCServices.objects.filter(writer = self.request.user)

class MPDCLView(generics.GenericAPIView):
    serializer_class = MPDCLSerializer
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]

    def get(self, request):
        try:
            mpdcl_data = MPDCL.objects.get(id=1)
            serializer = self.serializer_class(mpdcl_data)

            return custom_response.Success_response(msg="mpdcl data", data=serializer.data)
        except MPDCL.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        update_data = request.data
        mpdcl_data = MPDCL.objects.get(id=1)
        serializer = self.serializer_class(mpdcl_data, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg="mpdcl data", data=serializer.data)

class MPDCLServicesView(generics.ListCreateAPIView):
    serializer_class = MPDCLSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]

    def get_queryset(self):
        return MPDCL.objects.all()
    
    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="mpdcl service", data=serializer.data)

class MPDCLServicesDetialView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MPDCLSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, parsers.FormParser]
    lookup_field = "id"

    def get_queryset(self):
        return MPDCL.objects.filter(writer = self.request.user)

#PUBLIC VIEWS
class SectoralGroupPublicView(generics.ListAPIView):
    serializer_class = SectoralGroupSerializer

    def get_queryset(self):
        return SectoralGroup.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="sectoral groups", data=serializer.data)
    
class MRCServicePublicView(generics.ListAPIView):
    serializer_class = MRCServicesSerializer

    def get_queryset(self):
        return MRCServices.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="mrc service", data=serializer.data)
    
class MPDCLServicesPublicView(generics.ListAPIView):
    serializer_class = MPDCLSerializer

    def get_queryset(self):
        return MPDCL.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="mpdcl service", data=serializer.data)