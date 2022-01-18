import json
import os.path
import tempfile
from typing import List, Dict

import numpy
from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import ImageMetadata, Tag, ImageTags

numpy.random.seed(0)


class ImageTests(APITestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_static = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
        self.temp_static.cleanup()

    @staticmethod
    def get_random_image():
        image_array = numpy.random.rand(100, 100, 3) * 255
        image = Image.fromarray(image_array.astype('uint8')).convert('RGB')
        return image

    @staticmethod
    def get_same_image():
        image = Image.new('RGB', (100, 100))
        return image

    def add_image(self, description: str = "test", is_public: bool = True,
                  file_type: str = "jpg", tags: List[Dict[str, str]] = None, random: bool = True):
        if tags is None:
            tags = [{"name": "test1"}]

        # Create temporary image file for upload
        image = ImageTests.get_random_image() if random else ImageTests.get_same_image()
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        metadata = {
            "description": description,
            "is_public": is_public,
            "name": os.path.basename(tmp_file.name),
            "size": os.stat(tmp_file.name).st_size,
            "file_type": file_type,
            "tags": tags
        }

        with self.settings(
                IMAGE_STORAGE=os.path.join(self.temp_dir.name, ''),
                STATIC_ROOT=os.path.join(self.temp_static.name, '')
        ):
            response = self.client.post(
                reverse('add_image'),
                {
                    'file': tmp_file,
                    'metadata': json.dumps(metadata)
                }
            )
            return response


class AddImageTests(ImageTests):

    def test_add_image_too_long_file_type(self):
        response = self.add_image(file_type="testtesttesttest")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, ImageMetadata.objects.all().count())
        self.assertEqual(os.listdir(self.temp_dir.name), [])
        self.assertEqual(os.listdir(self.temp_static.name), [])
        self.assertIn('file_type', response.json())

    def test_add_image_duplicate(self):
        response1 = self.add_image(random=False)
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)

        # Add the same image again
        response2 = self.add_image(random=False)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)
        self.assertEqual(1, ImageMetadata.objects.all().count())
        self.assertIn('image_hash', response2.json())

    def test_add_image_valid(self):
        response = self.add_image()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, ImageMetadata.objects.all().count())

        image = ImageMetadata.objects.all()[0]
        self.assertEqual(os.listdir(self.temp_dir.name)[0], f"{image.image_id}.{image.file_type}")
        self.assertEqual(os.listdir(self.temp_static.name)[0], f"{image.image_id}.{image.file_type}")

    def test_add_image_3tags_created(self):
        response = self.add_image(tags=[{"name": "test1"}, {"name": "test2"}, {"name": "test3"}])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(3, Tag.objects.all().count())
        self.assertEqual(3, ImageTags.objects.all().count())

    def test_add_image_duplicate_tags(self):
        response = self.add_image(tags=[{"name": "test1"}, {"name": "test2"}, {"name": "test2"}])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # The server should filter out the duplicate "test2" tag
        self.assertEqual(2, Tag.objects.all().count())
        self.assertEqual(2, ImageTags.objects.all().count())

    def test_add_private_image_no_thumbnail(self):
        response = self.add_image(is_public=False)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        image = ImageMetadata.objects.all()[0]
        self.assertEqual(os.listdir(self.temp_dir.name)[0], f"{image.image_id}.{image.file_type}")
        self.assertEqual(os.listdir(self.temp_static.name), [])


class TagSearchTests(ImageTests):

    def setUp(self) -> None:
        super().setUp()

        tags_list = [
            [{"name": "t1"}, {"name": "t2"}, {"name": "t3"}],
            [{"name": "t1"}, {"name": "t2"}],
            [{"name": "t1"}, {"name": "t2"}],
            [{"name": "t1"}, {"name": "t3"}],
            [{"name": "t1"}],
            [{"name": "t3"}]
        ]

        # Create temporary image file for upload
        for i, tags in enumerate(tags_list, 1):
            self.add_image(tags=tags, )

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
