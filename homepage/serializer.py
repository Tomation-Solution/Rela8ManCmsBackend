from rest_framework import serializers
from .models import HomePageSlider


class HomePageSliderSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()

    class Meta:
        model = HomePageSlider
        fields = "__all__"

    def get_banner(self, obj):
        request = self.context.get("request")
        if obj.banner and request:
            return request.build_absolute_uri(obj.banner.url)
        return None

    def update(self, instance, validated_data):
        # Handle file upload manually since files are in request.FILES, not validated_data
        request = self.context.get("request")
        new_banner = request.FILES.get("banner") if request else None
        old_banner = instance.banner if new_banner else None

        # Update non-file fields from validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle banner update
        if new_banner:
            if old_banner:  # Delete old file if it exists
                old_banner.delete(save=False)
            instance.banner = new_banner

        instance.save()
        return instance
