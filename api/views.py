from typing import List, Tuple, Any, Dict

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
    if image.is_valid() and all(map(lambda item: item['is_valid'], tags)):
        image.save()
        for tag in tags:
            if tag['is_new']:
                tag['tag'].save()
            image_tag = ImageTags.objects.create(tag=tag['tag'], image=image)
            image_tag.save()
        return Response(image.data, status=status.HTTP_201_CREATED)
    print(image.errors, [tag['tag'].errors for tag in tags if tag['is_new']])
    return Response(image.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tags(tags) -> List[Dict[str, Any]]:
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
