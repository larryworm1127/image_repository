import imghdr
import json
import os.path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

import imagehash
from PIL import Image

from .client import add_image, Metadata, search_by_tags, get_image_file, search_by_thumbnail

__all__ = ['add_single_image', 'add_multiple_images', 'tag_search', 'get_image', 'thumbnail_search']


def add_single_image(path: str, description: str = "", is_public: bool = True,
                     tags: List[str] = None) -> None:
    """Add a single image to the image repository.

    Example:
    python main.py add_image pic.jpg --description="test" --tags=[tag1,tag2]

    :param path: the file path to the image.
    :param description: the description of the image.
    :param is_public: the visibility level of image in the repo.
    :param tags: the tags that categorize the image (example: [tag1,tag2])
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

    success, result = add_image(path, metadata)
    if success:
        print(f"Image {result['name']} created with ID {result['image_id']}")
    else:
        print(json.dumps(result, indent=2))


def add_multiple_images(path: str, descriptions: List[str] = None,
                        is_public: bool = True,
                        tags: List[List[str]] = None) -> None:
    """Add all images in the given directory to the image repository.

    :param path: the path to the directory
    :param descriptions: a list of descriptions for each image
    :param is_public: the visibility level of all the images in the repo.
    :param tags: a list of tag list that categorize each image in folder.
    """
    if not os.path.exists(path):
        print(f"Given {path} does not exists.")
        return

    if not os.path.isdir(path):
        print(f"Given {path} is not a directory.")
        return

    processes = []
    with ThreadPoolExecutor() as executor:
        for i, image in enumerate(os.listdir(path)):
            image_path = os.path.join(path, image)
            if imghdr.what(image_path) is None:
                continue

            description = "" if descriptions is None else descriptions[i]
            tag = [] if tags is None else tags[i]
            process = executor.submit(add_single_image, image_path, description, is_public, tag)
            processes.append(process)

    for task in as_completed(processes):
        if task.result():
            print(task.result())


def tag_search(tags: List[str]) -> None:
    """Search for images that have specific tags.

    This command only prints out the metadata for the images. To get
    the actual image, please use <get_image> command.

    :param tags: a list of tags to search the image by. (example: [tag1,tag2])
    """
    success, response = search_by_tags(tags)
    print(json.dumps(response, indent=2))


def thumbnail_search(path: str) -> None:
    """Search for images that are similar to the image at given path.

    This command only prints out the metadata for the images. To get
    the actual image, please use <get_image> command.

    :params path: the file path to the image.
    """
    if not os.path.exists(path):
        print(f"Given {path} does not exists.")
        return

    image_type = imghdr.what(path)
    if image_type is None:
        print(f"File at {path} is not an image.")
        return

    image = Image.open(path)
    image_hash = str(imagehash.average_hash(image, hash_size=32))
    success, result = search_by_thumbnail(image_hash)
    print(json.dumps(result, indent=2))


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

    success, result = get_image_file(image_id, path, os.path.isdir(path))
    if success:
        print(f"Image {result} downloaded successfully")
    else:
        print(json.dumps(result, indent=2))
