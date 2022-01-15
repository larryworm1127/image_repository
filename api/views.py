import json

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Tag, ImageTags
from api.serializer import ImageSerializer
from api.view_utils import process_image_metadata


class AddImage(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        print(request.data)
        image_file = request.data['file']
        metadata = json.loads(request.data['metadata'])
        metadata['location'] = "image_storage/"

        # Process metadata before saving image to storage
        success, message, image = process_image_metadata(metadata)
        if not success:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        with open(image.location, 'wb') as f:
            f.write(image_file.file.read())

        return Response(message, status=status.HTTP_201_CREATED)


class TagSearch(APIView):

    def get(self, request, tag):
        tag_obj = get_object_or_404(Tag.objects.get_queryset(), name=tag)
        image_tags = ImageTags.objects.filter(tag__name=tag_obj.name)
        image_data = [ImageSerializer(image_tag.image).data for image_tag in image_tags]
        return Response(image_data)


class GetImage(APIView):

    def get(self, request, image_id):
        return Response()
