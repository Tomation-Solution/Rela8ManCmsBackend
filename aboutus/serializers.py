from aboutus import models
from rest_framework import serializers
from rest_framework import exceptions


class AboutContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AboutContactUs
        fields = "__all__"


class AboutHistorySerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(required=False)
    history_image = serializers.ImageField(required=False)
    mission_image = serializers.ImageField(required=False)
    vision_image = serializers.ImageField(required=False)

    class Meta:
        model = models.AboutHistory
        exclude = ["writer"]

    def to_representation(self, instance):
        """Ensure images return full URLs in response."""
        request = self.context.get("request")
        representation = super().to_representation(instance)

        for image_field in [
            "main_image",
            "history_image",
            "mission_image",
            "vision_image",
        ]:
            image = getattr(instance, image_field)
            if image and request:
                representation[image_field] = request.build_absolute_uri(image.url)

        return representation


class AboutAdvocacySerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(required=False)

    class Meta:
        model = models.AboutAdvocacy
        exclude = ["writer"]

    def to_representation(self, instance):
        """Ensure images return full URLs in response."""
        request = self.context.get("request")
        representation = super().to_representation(instance)

        for image_field in [
            "main_image",
        ]:
            image = getattr(instance, image_field)
            if image and request:
                representation[image_field] = request.build_absolute_uri(image.url)

        return representation


class AboutAffilliateSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(required=False)

    class Meta:
        model = models.AboutAffilliate
        exclude = ["writer"]

    def to_representation(self, instance):
        """Ensure images return full URLs in response."""
        request = self.context.get("request")
        representation = super().to_representation(instance)

        for image_field in [
            "main_image",
        ]:
            image = getattr(instance, image_field)
            if image and request:
                representation[image_field] = request.build_absolute_uri(image.url)

        return representation


class AboutHowWeWorkSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(required=False)

    class Meta:
        model = models.AboutHowWeWork
        exclude = ["writer"]

    def to_representation(self, instance):
        """Ensure images return full URLs in response."""
        request = self.context.get("request")
        representation = super().to_representation(instance)

        for image_field in [
            "main_image",
        ]:
            image = getattr(instance, image_field)
            if image and request:
                representation[image_field] = request.build_absolute_uri(image.url)

        return representation


class AboutWhereWeOperateSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(required=False)

    class Meta:
        model = models.AboutWhereWeOperate
        exclude = ["writer"]

    def to_representation(self, instance):
        """Ensure images return full URLs in response."""
        request = self.context.get("request")
        representation = super().to_representation(instance)

        for image_field in [
            "main_image",
        ]:
            image = getattr(instance, image_field)
            if image and request:
                representation[image_field] = request.build_absolute_uri(image.url)

        return representation


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
    image = serializers.ImageField(required=False)

    def to_representation(self, instance):
        """Ensure images return full URLs in response."""
        request = self.context.get("request")
        representation = super().to_representation(instance)

        for image_field in ["image"]:
            image = getattr(instance, image_field)
            if image and request:
                representation[image_field] = request.build_absolute_uri(image.url)

        return representation

    class Meta:
        model = models.AboutOurExecutives
        exclude = ["writer"]
