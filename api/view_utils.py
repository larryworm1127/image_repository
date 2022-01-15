from typing import List, Dict, Any, Tuple, Optional

from django.core.exceptions import ObjectDoesNotExist

from api.models import Tag, ImageTags, ImageMetadata
from api.serializer import TagSerializer, ImageSerializer


def process_image_metadata(data) -> Tuple[Any, Optional[ImageMetadata]]:
    image_serializer = ImageSerializer(data=data)

    tags = get_tags(data['tags'])
    if image_serializer.is_valid() and all([tag['is_valid'] for tag in tags]):
        image = image_serializer.save()
        image.location = f"{image.location}{image.image_id}.{image.file_type}"
        image.save()

        for tag in tags:
            if tag['is_new']:
                tag['tag'] = tag['tag'].save()
            image_tag = ImageTags.objects.create(image=image, tag=tag['tag'])
            image_tag.save()

        return image_serializer.data, image

    return image_serializer.errors, None


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
