import json
import os.path
import tempfile
from typing import List, Dict

from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import ImageMetadata


class AddImageTests(APITestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create temporary image file for upload
        image = Image.new('RGB', (100, 100))
        self.tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(self.tmp_file)
        self.tmp_file.seek(0)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def add_image(self, description: str = "test", is_public: bool = False,
                  file_type: str = "jpg", tags: List[Dict[str, str]] = None):
        if tags is None:
            tags = [{"name": "test1"}]

        metadata = {
            "description": description,
            "is_public": is_public,
            "name": os.path.basename(self.tmp_file.name),
            "size": os.stat(self.tmp_file.name).st_size,
            "file_type": file_type,
            "tags": tags
        }

        with self.settings(IMAGE_STORAGE=os.path.join(self.temp_dir.name, '')):
            response = self.client.post(
                reverse('add_image'),
                {
                    'file': self.tmp_file,
                    'metadata': json.dumps(metadata)
                }
            )
            return response

    def test_add_image_invalid(self):
        response = self.add_image(file_type="testtesttesttest")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, len(ImageMetadata.objects.all()))
        self.assertEqual(os.listdir(self.temp_dir.name), [])
        self.assertIn('file_type', response.json())

    def test_add_image_valid(self):
        response = self.add_image()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, len(ImageMetadata.objects.all()))

        image = ImageMetadata.objects.all()[0]
        self.assertEqual(os.listdir(self.temp_dir.name)[0], f"{image.image_id}.{image.file_type}")


class TagSearchTests(APITestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()

        tags_list = [
            [{"name": "t1"}, {"name": "t2"}, {"name": "t3"}],
            [{"name": "t1"}, {"name": "t2"}],
            [{"name": "t1"}, {"name": "t2"}],
            [{"name": "t1"}, {"name": "t3"}],
            [{"name": "t1"}],
            [{"name": "t3"}]
        ]

        # Create temporary image file for upload
        for tags in tags_list:
            image = Image.new('RGB', (100, 100))
            tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
            image.save(tmp_file)
            tmp_file.seek(0)
            self.add_image(tmp_file, tags=tags)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def add_image(self, tmp_file, description: str = "test", is_public: bool = False,
                  file_type: str = "jpg", tags: List[Dict[str, str]] = None):
        if tags is None:
            tags = [{"name": "test1"}]

        metadata = {
            "description": description,
            "is_public": is_public,
            "name": os.path.basename(tmp_file.name),
            "size": os.stat(tmp_file.name).st_size,
            "file_type": file_type,
            "tags": tags
        }

        with self.settings(IMAGE_STORAGE=os.path.join(self.temp_dir.name, '')):
            response = self.client.post(
                reverse('add_image'),
                {
                    'file': tmp_file,
                    'metadata': json.dumps(metadata)
                }
            )
            return response

    def test_single_tag_search(self):
        response = self.client.get(
            reverse('tag_search'),
            {'tags': json.dumps(['t1'])},
        )

        response_json = response.json()
        self.assertEqual(5, len(response_json))

        image_ids = [image["image_id"] for image in response_json]
        self.assertEqual([1, 2, 3, 4, 5], image_ids)

    def test_multi_tag_search(self):
        response = self.client.get(
            reverse('tag_search'),
            {'tags': json.dumps(['t1', 't3'])},
        )

        response_json = response.json()
        self.assertEqual(2, len(response_json))

        image_ids = [image["image_id"] for image in response_json]
        self.assertEqual([1, 4], image_ids)
