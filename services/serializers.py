from services import models
from rest_framework import serializers
import secrets


class AllServicesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = models.AllServices
        fields = "__all__"


class RequestServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RequestService
        fields = "__all__"
        read_only_fields = ["ref"]

    def create(self, validated_data):

        while True:
            ref = secrets.token_urlsafe(20)
            object_with_similar_ref = models.RequestService.objects.filter(
                ref=ref)
            if not object_with_similar_ref:
                validated_data['ref'] = ref
                break

        service_request = models.RequestService.objects.create(
            **validated_data)

        return service_request


class SubscribeToNewsLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubscribeToNewsLetter
        fields = "__all__"
        read_only_fields = ["ref"]

    def create(self, validated_data):
        while True:
            ref = secrets.token_urlsafe(20)
            object_with_similar_ref = models.RequestService.objects.filter(
                ref=ref)
            if not object_with_similar_ref:
                validated_data['ref'] = ref
                break

        newletter_subscription = models.SubscribeToNewsLetter.objects.create(
            **validated_data)

        return newletter_subscription
