from rest_framework import serializers
from rest_framework import exceptions
from publications.models import Publication, PublicationType


class PublicationParagraphSerializer(serializers.Serializer):
    # id = serializers.IntegerField(required=False)
    header = serializers.CharField(allow_blank=True)
    value = serializers.CharField(allow_blank=True)


class PublicationSerializer(serializers.ModelSerializer):
    # paragraphs = serializers.SerializerMethodField()
    details = PublicationParagraphSerializer(
        many=True, required=True, allow_empty=False)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, required=False)
    readmore_link = serializers.URLField(required=False)

    image = serializers.ImageField(required=False)
    link = serializers.FileField(required=False)

    def validate(self, attrs):
        is_paid = attrs.get("is_paid", "")
        price = attrs.get("price", "")

        if is_paid == True:
            if not price:
                raise exceptions.ValidationError(
                    f"price must be provided on paid publications")
        elif is_paid == False:
            if price:
                raise exceptions.ValidationError(
                    f"price must not be provided on free publications")

        return super().validate(attrs)

    def create(self, validated_data):
        # list_of_paragraphs = validated_data.pop('details', [])
        # print(list_of_paragraphs)
        publication = Publication.objects.create(**validated_data)
        # for item in list_of_paragraphs:
        #     PublicationParagraph.objects.create(
        #         publication=publication,
        #         header=item.get('header', None),
        #         value=item.get('value', None),
        #     )
        return publication

    # def get_paragraphs(self, publication):
    #     return PublicationParagraph.objects.filter(publication=publication).values("id", "header", "value")

    # def update(self, instance, validated_data):
    #     # updating the individual details in their respective tables
    #     if 'details' in validated_data:
    #         details = validated_data.get("details")
    #         for item in details:
    #             item_id = item.get("id", None)
    #             publication_item, created = PublicationParagraph.objects.get_or_create(
    #                 publication=instance, id=item_id)
    #             publication_item.header = item.get(
    #                 "header", publication_item.header)
    #             publication_item.value = item.get(
    #                 "value", publication_item.value)

    #             publication_item.save()

    #         return instance

    #     # if no nested objects it should just update the pre-exisiting ones
    #     # return super(PublicationSerializer, self).update(instance, validated_data)
    #     return super().update(instance, validated_data)

    def update(self, instance, validated_data):
        is_paid = validated_data.get('is_paid', instance.is_paid)

        if is_paid == False:
            instance.price = 0.00

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
