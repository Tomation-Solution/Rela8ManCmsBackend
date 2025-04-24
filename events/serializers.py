from rest_framework import serializers, exceptions
from app.serializer import CloudinaryImageField
from events.models import Event, EventAndMediaContent, EventBanner


class EventBannerSerializer(serializers.ModelSerializer):
    banner_image = CloudinaryImageField(required=False)

    class Meta:
        model = EventBanner
        fields = ["id", "banner_image"]


class EventAndMediaContentSerializer(serializers.ModelSerializer):
    banner_image = CloudinaryImageField(required=False)
    main_image = CloudinaryImageField(required=False)
    news_image = CloudinaryImageField(required=False)
    publication_image = CloudinaryImageField(required=False)
    event_image = CloudinaryImageField(required=False)
    report_image = CloudinaryImageField(required=False)
    gallery_image = CloudinaryImageField(required=False)

    class Meta:
        model = EventAndMediaContent
        fields = [
            "id",
            "banner_image",
            "main_image",
            "news_image",
            "news_title",
            "news_description",
            "news_link_text",
            "publication_image",
            "publication_title",
            "publication_description",
            "publication_link_text",
            "event_image",
            "event_title",
            "event_description",
            "event_link_text",
            "report_image",
            "report_title",
            "report_description",
            "report_link_text",
            "gallery_image",
            "gallery_title",
            "gallery_description",
            "gallery_link_text",
        ]


from rest_framework import serializers, exceptions
from events.models import Event


class EventsSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)

    def validate(self, attrs):
        is_paid = attrs.get("is_paid", "")
        price = attrs.get("price", "")
        is_agm = attrs.get("is_agm", "")

        # paid/free consistency
        if is_paid is True and not price:
            raise exceptions.ValidationError(
                {"price": "Price must be provided for paid events."}
            )
        if is_paid is False and price:
            raise exceptions.ValidationError(
                {"price": "Price must not be provided for free events."}
            )

        # AGM-specific: must be free
        if is_agm is True and price:
            raise exceptions.ValidationError(
                {"price": "You can't provide a price for AGM events."}
            )

        return super().validate(attrs)

    def update(self, instance, validated_data):
        is_paid = validated_data.get("is_paid", instance.is_paid)
        is_agm = validated_data.get("is_agm", instance.is_agm)
        is_current_agm = validated_data.get("is_current_agm", instance.is_current_agm)

        # ensure free if unpaid
        if is_paid is False:
            validated_data["price"] = 0

        # AGM must always be free
        if is_agm:
            validated_data["price"] = 0
            validated_data["is_paid"] = False

        # Perform the update
        instance = super().update(instance, validated_data)

        # If this is now the current AGM, unset all others
        if is_agm and is_current_agm:
            Event.objects.filter(is_current_agm=True).exclude(pk=instance.pk).update(
                is_current_agm=False
            )
            instance.is_current_agm = True
            instance.save(update_fields=["is_current_agm"])

        return instance

    class Meta:
        model = Event
        exclude = ["writer"]
