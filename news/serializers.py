from rest_framework import serializers
from news.models import News


class NewsParagraphSerializer(serializers.Serializer):
    header = serializers.CharField(allow_blank=True)
    value = serializers.CharField(allow_blank=True)


class NewsSerializer(serializers.ModelSerializer):
    details = NewsParagraphSerializer(
        many=True, required=True, allow_empty=False)
    image = serializers.ImageField(required=False)

    def create(self, validated_data):
        news = News.objects.create(**validated_data)

        return news

    class Meta:
        model = News
        exclude = ["writer"]
