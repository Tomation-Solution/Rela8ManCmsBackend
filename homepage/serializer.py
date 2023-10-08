from rest_framework import serializers
from . import models


class HomePageSliderSerializer(serializers.ModelSerializer):

    class Meta:
        model =models.HomePageSlider
        fields ='__all__'