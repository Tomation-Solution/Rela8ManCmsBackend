from rest_framework import serializers
from gallery.models import Gallery, GalleryItems


class GalleryItemsSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    caption = serializers.CharField(max_length=300)
    image = serializers.ImageField(allow_empty_file=False)


class GallerySerializer(serializers.ModelSerializer):
    images = GalleryItemsSerializer(
        many=True, write_only=True, required=True, allow_empty=False)

    def create(self, validated_data):
        list_of_images = validated_data.pop("images", [])
        gallery = Gallery.objects.create(**validated_data)

        for item in list_of_images:
            GalleryItems.objects.create(gallery=gallery, caption=item.get(
                "caption"), image=item.get("image"))

        return gallery

    def update(self, instance, validated_data):
        if "images" in validated_data:
            images = validated_data.get("images")
            for item in images:
                item_id = item.get("id", None)
                gallery_item, created = GalleryItems.objects.get_or_create(
                    gallery=instance, id=item_id)
                gallery_item.caption = item.get(
                    "caption", gallery_item.caption)
                gallery_item.image = item.get(
                    "image", gallery_item.image)

                gallery_item.save()

            return instance

        return super(GallerySerializer, self).update(instance, validated_data)

    class Meta:
        model = Gallery
        exclude = ["writer"]
