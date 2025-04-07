from rest_framework import serializers, exceptions
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
    Logo = serializers.ImageField(required=False)
    slider_image1 = serializers.ImageField(required=False)
    slider_image2 = serializers.ImageField(required=False)
    slider_image3 = serializers.ImageField(required=False)
    history_image = serializers.ImageField(required=False)
    join_man_image = serializers.ImageField(required=False)

    class Meta:
        model = HomePage
        exclude = ["writer"]

    def get_image_url(self, instance, field_name):
        request = self.context.get("request")
        image = getattr(instance, field_name)
        return request.build_absolute_uri(image.url) if image and request else None

    def to_representation(self, instance):
        """Override to return full URLs for image fields"""
        data = super().to_representation(instance)
        image_fields = [
            "Logo",
            "slider_image1",
            "slider_image2",
            "slider_image3",
            "history_image",
            "join_man_image",
        ]

        for field in image_fields:
            data[field] = self.get_image_url(instance, field)

        return data


class WhyWeAreUniqueSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

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
