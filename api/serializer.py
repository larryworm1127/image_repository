from rest_framework import serializers

from api.models import ImageMetadata, Tag, ImageTags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class ImageSerializer(serializers.ModelSerializer):
    location = serializers.CharField(write_only=True)
    file_type = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = ImageMetadata
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        image_tags = ImageTags.objects.filter(image_id=ret['image_id'])
        ret['tags'] = [image_tag.tag.name for image_tag in image_tags]
        return ret
