import json
import os

import imagehash
from PIL import Image
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Tag, ImageTags, ImageMetadata
from api.serializer import ImageSerializer


class AddImage(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        metadata = json.loads(request.data['metadata'])
        metadata['location'] = settings.IMAGE_STORAGE

        # Create thumbnail and hash for image to prevent duplicates
        pil_image = Image.open(request.data['file'].file)
        thumbnail = pil_image.copy()
        thumbnail.thumbnail(size=settings.THUMBNAIL_SIZE)
        metadata['image_hash'] = str(imagehash.average_hash(thumbnail, hash_size=32))
        image_serializer = ImageSerializer(data=metadata)

        # Validate metadata before saving image to storage
        if not image_serializer.is_valid():
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Set image storage location using the generated unique ID
        image = image_serializer.save()
        image.location = f"{image.location}{image.image_id}.{image.file_type}"
        image.save()

        tags = set([tag['name'] for tag in metadata['tags']])  # Remove duplicate tags
        for tag in tags:
            tag_obj, _ = Tag.objects.get_or_create(name=tag)
            image_tag = ImageTags.objects.create(image=image, tag=tag_obj)
            image_tag.save()

        pil_image.save(image.location)

        # Save thumbnails of public image
        if image.is_public:
            thumbnail.save(os.path.join(settings.STATIC_ROOT, f"{image.image_id}.{image.file_type}"))

        return Response(image_serializer.data, status=status.HTTP_201_CREATED)


class TagSearch(APIView):

    def get(self, request: Request):
        image_tags = None
        for tag in json.loads(request.query_params.get('tags')):
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
