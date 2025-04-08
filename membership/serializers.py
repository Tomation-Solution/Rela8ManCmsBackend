from rest_framework import serializers, exceptions
from app.serializer import CleanedImageField
from membership.models import (
    WhyJoinMan,
    JoiningStep,
    FAQs,
    HomePage,
    WhyWeAreUnique,
    OurMembers,
    Advertisement,
)


class WhyJoinManSerializers(serializers.ModelSerializer):
    header = serializers.CharField(max_length=300)

    class Meta:
        model = WhyJoinMan
        exclude = ["writer"]


class JoiningStepSerializer(serializers.ModelSerializer):
    step_name = serializers.CharField(max_length=300, required=True)
    step_list = serializers.JSONField(required=False)
    step_description = serializers.CharField(required=False)
    step_extras = serializers.JSONField(required=False)

    class Meta:
        model = JoiningStep
        exclude = ["writer"]


class FAQsSerializer(serializers.ModelSerializer):
    header = serializers.CharField(max_length=400, required=True)
    content = serializers.JSONField(required=True)

    class Meta:
        model = FAQs
        exclude = ["writer"]


class HomePageSerializer(serializers.ModelSerializer):
    Logo = CleanedImageField(required=False)
    slider_image1 = CleanedImageField(required=False)
    slider_image2 = CleanedImageField(required=False)
    slider_image3 = CleanedImageField(required=False)
    history_image = CleanedImageField(required=False)
    join_man_image = CleanedImageField(required=False)

    class Meta:
        model = HomePage
        exclude = ["writer"]


class WhyWeAreUniqueSerializer(serializers.ModelSerializer):
    image = CleanedImageField(required=False)

    class Meta:
        model = WhyWeAreUnique
        exclude = ["writer"]


class OurMembersSerializer(serializers.ModelSerializer):
    website = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = OurMembers
        exclude = ["writer"]


class AdvertismentViewSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        number_of_adverts = Advertisement.objects.count()
        if number_of_adverts >= 3:
            raise exceptions.ValidationError("maximum of three adds can be created")
        return super().validate(attrs)

    class Meta:
        model = Advertisement
        fields = "__all__"
