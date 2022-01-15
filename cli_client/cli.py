import imghdr
import os.path
from typing import List

import fire

from client import add_image, Metadata


def add_single_image(path: str, description: str = "", is_public: bool = True,
                     tags: List[str] = None) -> None:
    """Add a single image to the image repository.

    :param path: the file path to the image.
    :param description: the description of the image.
    :param is_public: the visibility level of image in the repo.
    :param tags: the tags that categorize the image
    :return:
    """
    if not os.path.exists(path):
        print(f"Given {path} does not exists.")
        return

    image_type = imghdr.what(path)
    if image_type is None:
        print(f"File at {path} is not an image.")
        return

    metadata = Metadata(
        description=description,
        is_public=is_public,
        name=os.path.basename(path),
        size=os.stat(path).st_size,
        file_type=image_type,
        tags=[] if tags is None else [{"name": tag} for tag in tags]
    )

    success, message = add_image(path, metadata)
    print(message)


def add_multiple_images(path: str, descriptions: List[str] = None,
                        is_public: bool = True,
                        tags: List[List[str]] = None) -> None:
    """Add all images in the given directory to the image repository.

    :param path: the path to the directory
    :param descriptions: a list of descriptions for each image
    :param is_public:
    :param tags:
    :return:
    """
    if not os.path.exists(path):
        print(f"Given {path} does not exists.")
        return

    if not os.path.isdir(path):
        print(f"Given {path} is not a directory.")
        return

    for i, image in enumerate(os.listdir(path)):
        if imghdr.what(image) is not None:
            add_single_image(image, descriptions[i], is_public, tags[i])


if __name__ == '__main__':
    fire.Fire({
        'add_image': add_single_image,
        'add_images': add_multiple_images
    })
