from agmcms import models
from rest_framework import serializers


class AGMHomepageCMSSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AGMHomepageCMS
        fields = "__all__"


class AGMProgrammeCMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AGMProgrammeCMS
        fields = "__all__"


class AGMProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AGMPrograms
        fields = "__all__"


class AGMSpeakersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AGMSpeakers
        fields = "__all__"


class AGMVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AGMVenue
        fields = "__all__"


class AGMExhibitionCMSSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AGMExhibitionCMS
        fields = "__all__"


class AGMPreviousExhibitionAndCompanyImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AGMPreviousExhibitionAndCompanyImages
        fields = "__all__"


class AGMFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AGMFAQ
        fields = "__all__"
