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
            gallery=instance)
        list_of_images = []
        for i in gallery_images:
            list_of_images.append(
                {"id": i.id, "caption": i.caption, "image": i.image.url})
        return list_of_images

    def create(self, validated_data):
        list_of_images = validated_data.pop("images", [])
        gallery = Gallery.objects.create(**validated_data)

        for item in list_of_images:
            GalleryItems.objects.create(gallery=gallery, caption=item.get(
                "caption"), image=item.get("image"))

        return gallery

    class Meta:
        model = Gallery
        exclude = ["writer"]


class GalleryRenameSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)


class GalleryItemSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(required=True)
    image = Base64ImageField(required=True)
    gallery = serializers.PrimaryKeyRelatedField(
        queryset=Gallery.objects.all(), allow_null=False, required=False)

    class Meta:
        model = GalleryItems
        fields = "__all__"
