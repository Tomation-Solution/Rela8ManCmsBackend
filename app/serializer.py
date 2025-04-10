from rest_framework import serializers


class CloudinaryImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None

        url = super().to_representation(value)
        print("url >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(url)

        # Cloudinary already gives a full URL
        return url if url.startswith("http") else None
