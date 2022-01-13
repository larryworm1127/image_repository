import json
from typing import List, Any, Dict

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import ImageMetadata, Tag, ImageTags
from api.serializer import ImageSerializer, TagSerializer


# @api_view(['POST'])
# def add_image_metadata(request):
#     image = ImageSerializer(data=request.data)
#     tags = get_tags(request.data['tags'])
#     if image.is_valid() and all([tag['is_valid'] for tag in tags]):
#         image_inst: ImageMetadata = image.save()
#         for tag in tags:
#             if tag['is_new']:
#                 tag['tag'] = tag['tag'].save()
#             image_tag = ImageTags.objects.create(image=image_inst, tag=tag['tag'])
#             image_tag.save()
#
#         image.data['id'] = image_inst.image_id
#         return Response(image.data, status=status.HTTP_201_CREATED)
#
#     errors = [tag['tag'].error for tag in tags if tag['is_new']] + [image.errors]
#     return Response(errors, status=status.HTTP_400_BAD_REQUEST)


def process_image_metadata(data):
    image_serializer = ImageSerializer(data=data)

    tags = get_tags(data['tags'])
    if image_serializer.is_valid() and all([tag['is_valid'] for tag in tags]):
        image = image_serializer.save()
        image.location = f"{image.location}{image.image_id}.{image.file_type}"
        print(image.location)
        image.save()

        for tag in tags:
            if tag['is_new']:
                tag['tag'] = tag['tag'].save()
            image_tag = ImageTags.objects.create(image=image, tag=tag['tag'])
            image_tag.save()

        return True, image_serializer.data, image

    errors = [tag['tag'].error for tag in tags if tag['is_new']] + [image_serializer.errors]
    return False, errors, None


class AddImage(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        print(request.data)
        image_file: InMemoryUploadedFile = request.data['file']
        metadata = json.loads(request.data['metadata'])
        metadata['location'] = "image_storage/"
        print(metadata)
        success, message, image = process_image_metadata(metadata)
        if not success:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        with open(image.location, 'wb') as f:
            f.write(image_file.file.read())

        return Response(message, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def search(request):
    return Response({}, status=status.HTTP_200_OK)


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
    queryset = ImageMetadata.objects.all()
    serializer_class = ImageSerializer
