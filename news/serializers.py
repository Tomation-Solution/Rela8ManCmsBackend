from rest_framework import serializers

from app.serializer import CloudinaryImageField
from news.models import News, UploadedImage


class NewsParagraphSerializer(serializers.Serializer):
    header = serializers.CharField(allow_blank=True)
    value = serializers.CharField(allow_blank=True)


class NewsSerializer(serializers.ModelSerializer):
    details = serializers.JSONField(required=False)
    image = serializers.SerializerMethodField()  # Ensures full URL
    title = serializers.CharField(required=False, allow_blank=True)
    news_content = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = News
        exclude = ["writer"]

    def get_image(self, obj):
        """
        Return the full URL of the image.
        """
        if obj.image:
            request = self.context.get("request")
            return (
                request.build_absolute_uri(obj.image.url) if request else obj.image.url
            )
        return None

    def create(self, validated_data):
        return News.objects.create(**validated_data)


class NewsUpdateSerializer(serializers.ModelSerializer):
    details = serializers.JSONField(required=False)
    image = CloudinaryImageField(
        required=False, allow_null=True
    )  # Allow empty image field
    title = serializers.CharField(required=False, allow_blank=True)
    news_content = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = News
        exclude = ["writer"]

    def update(self, instance, validated_data):
        request = self.context.get("request")

        # Check if a new image was uploaded
        if request and "image" in request.FILES:
            instance.image = request.FILES["image"]

        if "link" in request.FILES:
            instance.link = request.FILES["link"]

        # Update other fields
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ["id", "image", "uploaded_at"]
