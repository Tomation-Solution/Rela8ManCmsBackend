from rest_framework import serializers
from reports.models import Reports


class ReportsParagraphSerializer(serializers.Serializer):
    header = serializers.CharField(allow_blank=True)
    value = serializers.CharField(allow_blank=True)


class ReportsSerializer(serializers.ModelSerializer):
    details = ReportsParagraphSerializer(
        many=True, required=True, allow_empty=False)
    readmore_link = serializers.URLField(required=False)
    link = serializers.FileField(required=False)

    def create(self, validated_data):
        report = Reports.objects.create(**validated_data)
        return report

    class Meta:
        model = Reports
        exclude = ["writer"]
