from rest_framework import serializers
from app.serializer import CleanedImageField
from reports.models import Reports


class ReportsParagraphSerializer(serializers.Serializer):
    header = serializers.CharField(allow_blank=True)
    value = serializers.CharField(allow_blank=True)


class ReportsSerializer(serializers.ModelSerializer):
    image = CleanedImageField(required=False)
    link = serializers.FileField(required=False)
    readmore_link = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Reports
        exclude = ["writer"]

    def create(self, validated_data):
        request = self.context.get("request")
        writer = request.user if request else None
        return Reports.objects.create(writer=writer, **validated_data)

    def update(self, instance, validated_data):
        # Only update fields if they are in the request data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
