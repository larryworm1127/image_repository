import json

from django.http import FileResponse
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Tag, ImageTags, ImageMetadata
from api.serializer import ImageSerializer
from api.view_utils import process_image_metadata


class AddImage(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        print(request.data)
        image_file = request.data['file']
        metadata = json.loads(request.data['metadata'])
        metadata['location'] = settings.IMAGE_STORAGE

        # Process metadata before saving image to storage
        message, image = process_image_metadata(metadata)
        if image is None:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        with open(image.location, 'wb') as f:
            f.write(image_file.file.read())

        return Response(message, status=status.HTTP_201_CREATED)


class TagSearch(APIView):

    def get(self, request):
        image_tags = None
        for tag in request.data:
            try:
                tag_obj = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                raise NotFound(f"Tag {tag} does not exist")

            if image_tags is None:
                image_tags = ImageTags.objects.filter(tag__name=tag_obj.name).values('image_id')
                continue

            curr = ImageTags.objects.filter(tag__name=tag_obj.name).values('image_id')
            image_tags = image_tags.intersection(curr)

        image_data = [
            ImageSerializer(
                ImageMetadata.objects.get(image_id=item['image_id'])
            ).data
            for item in image_tags
        ]
        return Response(image_data)


class GetImage(APIView):

    def get(self, request, image_id):
        try:
            image = ImageMetadata.objects.get(image_id=image_id)
        except ImageMetadata.DoesNotExist:
            raise NotFound(f"Image not found with ID {image_id}")

        return FileResponse(
            open(image.location, 'rb'),
            filename=image.name,
            content_type=f'image/{image.file_type}'
        )
