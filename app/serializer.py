from rest_framework import serializers


class CloudinaryImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None

        url = super().to_representation(value)
        # Cloudinary already gives a full URL
        return url if url.startswith("http") else None
