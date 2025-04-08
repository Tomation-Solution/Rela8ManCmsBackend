from aboutus import models
from rest_framework import serializers
from rest_framework import exceptions

from app.serializer import CleanedImageField


class AboutContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AboutContactUs
        fields = "__all__"


class AboutHistorySerializer(serializers.ModelSerializer):
    main_image = CleanedImageField(required=False)
    history_image = CleanedImageField(required=False)
    mission_image = CleanedImageField(required=False)
    vision_image = CleanedImageField(required=False)

    class Meta:
        model = models.AboutHistory
        exclude = ["writer"]


class AboutAdvocacySerializer(serializers.ModelSerializer):
    main_image = CleanedImageField(required=False)

    class Meta:
        model = models.AboutAdvocacy
        exclude = ["writer"]


class AboutAffilliateSerializer(serializers.ModelSerializer):
    main_image = CleanedImageField(required=False)

    class Meta:
        model = models.AboutAffilliate
        exclude = ["writer"]


class AboutHowWeWorkSerializer(serializers.ModelSerializer):
    main_image = CleanedImageField(required=False)

    class Meta:
        model = models.AboutHowWeWork
        exclude = ["writer"]


class AboutWhereWeOperateSerializer(serializers.ModelSerializer):
    main_image = CleanedImageField(required=False)

    class Meta:
        model = models.AboutWhereWeOperate
        exclude = ["writer"]


class AboutWhereWeOperateOfficeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=300, required=True)
    email = serializers.JSONField(required=True)
    phone_no = serializers.JSONField(required=True)
    address = serializers.CharField(max_length=300, required=True)
    website = serializers.URLField(required=False)

    class Meta:
        model = models.AboutWhereWeOperateOffice
        exclude = ["writer"]


class AboutWhereWeOperateBranchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=300, required=True)
    manager_name = serializers.CharField(max_length=300, required=True)
    title = serializers.CharField(max_length=300, required=True)
    email = serializers.JSONField(required=True)
    address = serializers.CharField(max_length=300, required=True)

    class Meta:
        model = models.AboutWhereWeOperateBranch
        exclude = ["writer"]


class AboutOurExecutivesSerializer(serializers.ModelSerializer):
    image = CleanedImageField(required=False)

    class Meta:
        model = models.AboutOurExecutives
        exclude = ["writer"]
