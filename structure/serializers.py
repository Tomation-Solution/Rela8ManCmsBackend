from structure.models import SectoralGroup, MRC, MRCServices, MPDCL, MPDCLServices
from rest_framework import serializers

class SectoralGroupSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required = False)

    class Meta:
        model = SectoralGroup
        exclude = ["writer"]

class HeaderDescriptionSerializer(serializers.Serializer):
    header = serializers.CharField(required= True)
    description = serializers.CharField(required=True)

class MRCSerializer(serializers.ModelSerializer):
    objectives_card = HeaderDescriptionSerializer(many=True, required=True, allow_empty=False)

    class Meta:
        model = MRC
        exclude = ["writer"]

class MRCServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MRCServices
        exclude = ["writer"]


class MPDCLSerializer(serializers.ModelSerializer):
    renewable_items = HeaderDescriptionSerializer(many=True, allow_empty=False, required=True)

    class Meta:
        model = MPDCL
        exclude = ["writer"]
    
class MPDCLServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MPDCLServices
        exclude = ["writer"]