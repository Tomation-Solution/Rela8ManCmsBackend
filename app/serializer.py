from rest_framework import serializers
from django.conf import settings
from urllib.parse import urljoin


class CleanedImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None

        url = super().to_representation(value)

        # Fix incorrect prefix if present
        if "/media/media/" in url:
            url = url.replace("/media/media/", "/media/")

        # Add domain if needed
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(url)
        else:
            return urljoin(getattr(settings, "SITE_URL", ""), url)
