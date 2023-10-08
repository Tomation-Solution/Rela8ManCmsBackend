from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializer
from utils import custom_parsers, custom_response, custom_permissions
from rest_framework.decorators  import action
from rest_framework.response import Response


class HomePageSliderViewset(viewsets.ModelViewSet):
    queryset = models.HomePageSlider.objects.all()
    serializer_class= serializer.HomePageSliderSerializer
    permission_classes =[ custom_permissions.IsAuthenticated]


    @action(detail=False, methods=['get'],permission_classes=[])
    def get_slider(self, request, pk=None):
        data = models.HomePageSlider.objects.all()
        serialize = self.serializer_class(instance=data,many=True)
        clean_data= serialize.data 
        return Response(data=clean_data,)