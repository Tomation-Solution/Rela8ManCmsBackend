from app.serializer import CloudinaryImageField
from services import models
from rest_framework import serializers
import secrets
import re


class AllServicesSerializer(serializers.ModelSerializer):
    image = CloudinaryImageField(required=False)

    class Meta:
        model = models.AllServices
        fields = "__all__"


class ServiceBannerSerializer(serializers.ModelSerializer):
    banner_image = CloudinaryImageField(required=False)

    class Meta:
        model = models.ServiceBanner
        fields = "__all__"


class RequestServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RequestService
        fields = "__all__"
        read_only_fields = ["ref"]

    def create(self, validated_data):

        while True:
            ref = secrets.token_urlsafe(20)
            object_with_similar_ref = models.RequestService.objects.filter(ref=ref)
            if not object_with_similar_ref:
                validated_data["ref"] = ref
                break

        service_request = models.RequestService.objects.create(**validated_data)

        return service_request


class SubscribeToNewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscribeToNewsLetter
        fields = "__all__"
        read_only_fields = ["ref", "is_verified"]

    def validate_email(self, value):
        email_regex = r"(^[\w\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format")
        return value

    def create(self, validated_data):
        while True:
            ref = secrets.token_urlsafe(20)
            if not models.SubscribeToNewsLetter.objects.filter(ref=ref).exists():
                validated_data["ref"] = ref
                break
        return models.SubscribeToNewsLetter.objects.create(**validated_data)


from .models import NewsletterUIConfig, ServiceBanner


class NewsletterUIConfigSerializer(serializers.ModelSerializer):
    form_image = serializers.SerializerMethodField()

    class Meta:
        model = NewsletterUIConfig
        fields = ["header", "description", "btn_text", "form_image"]

    def get_form_image(self, obj):
        request = self.context.get("request")
        if obj.form_image and hasattr(obj.form_image, "url"):
            return (
                request.build_absolute_uri(obj.form_image.url)
                if request
                else obj.form_image.url
            )
        return None
