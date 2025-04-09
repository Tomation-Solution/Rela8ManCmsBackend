from rest_framework import serializers
from django.conf import settings
from urllib.parse import urljoin


class CleanedImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None

        # Fix the .name BEFORE calling super()
        if value.name.startswith("media/"):
            value.name = value.name[len("media/") :]

        url = super().to_representation(value)

        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(url)
        else:
            return urljoin(getattr(settings, "SITE_URL", ""), url)
