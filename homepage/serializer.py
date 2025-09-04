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


from .models import FooterContent


class FooterContentSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = FooterContent
        fields = [
            "id",
            "logo",
            "company_name",
            "address",
            "email",
            "phone",
            "webmail_url",
            "branch_network_url",
            "services_url",
            "facebook_url",
            "linkedin_url",
            "twitter_url",
            "instagram_url",
            "youtube_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_logo(self, obj):
        request = self.context.get("request")
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None

    def update(self, instance, validated_data):
        # Handle file upload manually since files are in request.FILES, not validated_data
        request = self.context.get("request")
        new_logo = request.FILES.get("logo") if request else None
        old_logo = instance.logo if new_logo else None

        # Update non-file fields from validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle logo update
        if new_logo:
            if old_logo:  # Delete old file if it exists
                old_logo.delete(save=False)
            instance.logo = new_logo

        instance.save()
        return instance

    def validate_email(self, value):
        """Validate email format"""
        if not value:
            raise serializers.ValidationError("Email is required")
        return value

    def validate_company_name(self, value):
        """Validate company name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Company name is required")
        return value.strip()

    def validate_address(self, value):
        """Validate address"""
        if not value or not value.strip():
            raise serializers.ValidationError("Address is required")
        return value.strip()

    def validate_phone(self, value):
        """Validate phone"""
        if not value or not value.strip():
            raise serializers.ValidationError("Phone is required")
        return value.strip()
