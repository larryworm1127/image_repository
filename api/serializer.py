from rest_framework import serializers

from api.models import ImageMetadata, ImageTags


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for image metadata model. Certain fields are set to write only
    as we don't want to expose them to the end users.
    """

    class Meta:
        model = ImageMetadata
        fields = "__all__"
        extra_kwargs = {
            'location': {'write_only': True},
            'file_type': {'write_only': True},
            'image_hash': {'write_only': True}
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        image_tags = ImageTags.objects.filter(image_id=ret['image_id'])
        ret['tags'] = [image_tag.tag.name for image_tag in image_tags]
        return ret
