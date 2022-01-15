import json
import os.path
import tempfile

from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import ImageMetadata


class AddImageTests(APITestCase):

    def test_(self):
        # Create temporary image file for upload
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        metadata = {
            "description": "test",
            "is_public": False,
            "name": os.path.basename(tmp_file.name),
            "size": os.stat(tmp_file.name).st_size,
            "file_type": "jpg",
            "tags": [{"name": "test1"}, {"name": "test2"}]
        }

        response = self.client.post(
            '/api/images',
            {
                'file': tmp_file,
                'metadata': json.dumps(metadata)
            }
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, len(ImageMetadata.objects.all()))
