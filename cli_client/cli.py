import imghdr
import os.path
from typing import List

from .client import add_image, Metadata, search_by_tags, get_image_file


__all__ = ['add_single_image', 'add_multiple_images', 'tag_search', 'get_image']


def add_single_image(path: str, description: str = "", is_public: bool = True,
                     tags: List[str] = None) -> None:
    """Add a single image to the image repository.

    :param path: the file path to the image.
    :param description: the description of the image.
    :param is_public: the visibility level of image in the repo.
    :param tags: the tags that categorize the image
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

    message = add_image(path, metadata)
    print(message)


def add_multiple_images(path: str, descriptions: List[str] = None,
                        is_public: bool = True,
                        tags: List[List[str]] = None) -> None:
    """Add all images in the given directory to the image repository.

    :param path: the path to the directory
    :param descriptions: a list of descriptions for each image
    :param is_public:
    :param tags:
    """
    if not os.path.exists(path):
        print(f"Given {path} does not exists.")
        return

    if not os.path.isdir(path):
        print(f"Given {path} is not a directory.")
        return

    for i, image in enumerate(os.listdir(path)):
        image_path = os.path.join(path, image)
        if imghdr.what(image_path) is not None:
            description = "" if descriptions is None else descriptions[i]
            tag = [] if tags is None else tags[i]
            add_single_image(image_path, description, is_public, tag)


def tag_search(tags: List[str]) -> None:
    """Search for images that have specific tags.

    This command only prints out the metadata for the images. To get
    the actual image, please use <get_image> command.

    :param tags: a list of tags to search the image by.
    """
    response = search_by_tags(tags)
    print(response)


def get_image(image_id: int, path: str = ".") -> None:
    """Downloads an image from the repository given the ID.

    :param image_id: the ID of the image.
    :param path: the file path to save the image to.
    """
    if not os.path.exists(path):
        print(f"Given {path} does not exists.")
        return

    if path == ".":
        path = os.path.abspath(path)

    response = get_image_file(image_id, path, os.path.isdir(path))
    print(response)
