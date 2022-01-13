from rest_framework import serializers

from api.models import ImageMetadata, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMetadata
        fields = "__all__"
