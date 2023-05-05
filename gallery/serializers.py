from rest_framework import serializers
from gallery.models import Gallery, GalleryItems
from drf_extra_fields.fields import Base64ImageField


class GalleryItemsSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    caption = serializers.CharField(max_length=300)
    image = Base64ImageField(required=True)


class GallerySerializer(serializers.ModelSerializer):
    images = GalleryItemsSerializer(
        many=True, write_only=True, required=True, allow_empty=False)
    gallery_images = serializers.SerializerMethodField()

    def get_gallery_images(self, instance):
        gallery_images = GalleryItems.objects.filter(
            gallery=instance).values("id", "caption", "image")
        print(instance)
        return gallery_images

    def create(self, validated_data):
        list_of_images = validated_data.pop("images", [])
        gallery = Gallery.objects.create(**validated_data)

        for item in list_of_images:
            GalleryItems.objects.create(gallery=gallery, caption=item.get(
                "caption"), image=item.get("image"))

        return gallery

    # def update(self, instance, validated_data):
    #     if "images" in validated_data:
    #         images = validated_data.get("images")
    #         for item in images:
    #             item_id = item.get("id", None)
    #             gallery_item, created = GalleryItems.objects.get_or_create(
    #                 gallery=instance, id=item_id)
    #             gallery_item.caption = item.get(
    #                 "caption", gallery_item.caption)
    #             gallery_item.image = item.get(
    #                 "image", gallery_item.image)

    #             gallery_item.save()

    #         return instance

    #     return super(GallerySerializer, self).update(instance, validated_data)

    class Meta:
        model = Gallery
        exclude = ["writer"]


class GalleryRenameSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)


class GalleryItemSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(required=True)
    image = Base64ImageField(required=True)

    class Meta:
        model = GalleryItems
        fields = "__all__"
