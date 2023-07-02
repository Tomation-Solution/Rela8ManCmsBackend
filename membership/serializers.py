from rest_framework import serializers
from membership.models import WhyJoinMan, JoiningStep, FAQs, HomePage, WhyWeAreUnique, OurMembers


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
    slider_welcome_message = serializers.CharField(required=True)
    slider_vision_message = serializers.CharField(required=True)
    slider_mission_message = serializers.CharField(required=True)

    vision_intro = serializers.JSONField(required=True)
    mission_intro = serializers.JSONField(required=True)
    advocacy_intro = serializers.JSONField(required=True)
    history_intro = serializers.JSONField(required=True)
    why_join_intro = serializers.JSONField(required=True)
    members_intro = serializers.JSONField(required=True)

    slider_image1 = serializers.ImageField(required=False)
    slider_image2 = serializers.ImageField(required=False)
    slider_image3 = serializers.ImageField(required=False)

    class Meta:
        model = HomePage
        exclude = ["writer"]


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
