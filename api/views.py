from typing import List, Any, Dict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Image, Tag, ImageTags
from api.serializer import ImageSerializer, TagSerializer


@api_view(['POST'])
def add_image(request):
    image = ImageSerializer(data=request.data)
    tags = get_tags(request.data['tags'])
    if image.is_valid() and all([tag['is_valid'] for tag in tags]):
        image_inst = image.save()
        for tag in tags:
            if tag['is_new']:
                tag['tag'] = tag['tag'].save()
            image_tag = ImageTags.objects.create(image=image_inst, tag=tag['tag'])
            image_tag.save()

        new_data = [tag['tag'].data for tag in tags if tag['is_new']] + [image.data]
        return Response(new_data, status=status.HTTP_201_CREATED)

    errors = [tag['tag'].error for tag in tags if tag['is_new']] + [image.errors]
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


def get_tags(tags) -> List[Dict[str, Any]]:
    """
    Determine whether the input tags exist or not.

    If tag does not exist, then we create new one. Otherwise, we
    assign the existing tag object to the image.

    :param tags: list of tag names associated with the new image
    :return: a dictionary containing tag object, valid status, and new tag status.
    """
    result = []
    for tag in tags:
        try:
            exist = Tag.objects.get(name=tag['name'])
            result.append(
                {'tag': exist, 'is_valid': True, 'is_new': False}
            )
        except ObjectDoesNotExist:
            new_tag = TagSerializer(data=tag)
            result.append(
                {'tag': new_tag, 'is_valid': new_tag.is_valid(), 'is_new': True}
            )

    return result


class ImageDetail(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
