from app.serializer import CloudinaryImageField
from structure.models import SectoralGroup, MRC, MRCServices, MPDCL, MPDCLServices
from rest_framework import serializers
from .models import MrcContactPage, SectorialBanner


class SectorialBannerSerializer(serializers.ModelSerializer):
    banner_image = CloudinaryImageField(required=False)

    class Meta:
        model = SectorialBanner
        fields = ["id", "banner_image"]


class MrcContactPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MrcContactPage
        fields = [
            "get_in_touch_header",
            "get_in_touch_desc",
            "address_header",
            "address",
            "phone",
            "email",
            "link_text",
            "business_hours_header",
            "business_hours",
        ]


class SectoralGroupSerializer(serializers.ModelSerializer):
    image = CloudinaryImageField(required=False)

    class Meta:
        model = SectoralGroup
        exclude = ["writer"]


class HeaderDescriptionSerializer(serializers.Serializer):
    header = serializers.CharField(required=True)
    description = serializers.CharField(required=True)


class MRCSerializer(serializers.ModelSerializer):
    banner_image = CloudinaryImageField()
    objectives_card = HeaderDescriptionSerializer(
        many=True, required=True, allow_empty=False
    )

    class Meta:
        model = MRC
        exclude = ["writer"]


class MRCServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MRCServices
        exclude = ["writer"]


class MPDCLSerializer(serializers.ModelSerializer):
    banner_image = CloudinaryImageField()
    renewable_items = HeaderDescriptionSerializer(
        many=True, allow_empty=False, required=True
    )

    class Meta:
        model = MPDCL
        exclude = ["writer"]


class MPDCLServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MPDCLServices
        exclude = ["writer"]
