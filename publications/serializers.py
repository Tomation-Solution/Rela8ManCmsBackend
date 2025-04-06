from rest_framework import serializers
from rest_framework import exceptions
from publications.models import Publication, PublicationType


class PublicationParagraphSerializer(serializers.Serializer):
    # id = serializers.IntegerField(required=False)
    header = serializers.CharField(allow_blank=True)
    value = serializers.CharField(allow_blank=True)


class PublicationSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, required=False, allow_null=True
    )
    readmore_link = serializers.URLField(
        required=False, allow_blank=True, allow_null=True
    )
    image = serializers.ImageField(required=False, allow_null=True)
    link = serializers.FileField(required=False, allow_null=True)

    # New fields
    publication_content = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    def validate(self, attrs):
        is_paid = attrs.get("is_paid", None)
        price = attrs.get("price", None)

        if is_paid is True and (price is None or price == 0.00):
            raise serializers.ValidationError(
                "Price must be provided for paid publications."
            )
        if is_paid is False and price:
            raise serializers.ValidationError(
                "Price must not be provided for free publications."
            )

        return super().validate(attrs)

    def create(self, validated_data):
        publication = Publication.objects.create(**validated_data)
        return publication

    def update(self, instance, validated_data):
        is_paid = validated_data.get("is_paid", instance.is_paid)

        if is_paid is False:
            instance.price = 0.00  # Ensure price is set to zero for free publications

        return super().update(instance, validated_data)

    class Meta:
        model = Publication
        exclude = ["writer"]


class PublicationSerializerPaid(serializers.ModelSerializer):

    class Meta:
        model = Publication
        fields = ["id", "name", "title", "price", "image"]


class PublicationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicationType
        exclude = ["writer"]
