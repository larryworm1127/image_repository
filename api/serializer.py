from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from api.models import Image, Tag, ImageTags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class ImageSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True)

    class Meta:
        model = Image
        fields = ('description', 'is_public', 'url',)

    # def create(self, validated_data):
    #     print(validated_data)
    #     tags = validated_data.pop('tags')
    #     image = Image.objects.create(**validated_data)
    #     for tag in tags:
    #         try:
    #             exist = Tag.objects.get(name=tag['name'])
    #             ImageTags.objects.create(tag=exist, image=image)
    #         except ObjectDoesNotExist:
    #             new_tag = Tag.objects.create(name=tag['name'])
    #             ImageTags.objects.create(tag=new_tag, image=image)
    #
    #     return image
