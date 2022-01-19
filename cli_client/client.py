import json
import os.path
import re
from collections import namedtuple
from typing import List, Any, Tuple

import requests

__all__ = [
    'Metadata',
    'add_image',
    'search_by_tags',
    'search_by_thumbnail',
    'get_image_file'
]

Metadata = namedtuple(
    'Metadata',
    [
        "description",
        "is_public",
        "name",
        "size",
        "file_type",
        "tags"
    ]
)


def add_image(path: str, metadata: Metadata) -> Tuple[bool, Any]:
    """
    Function for making POST request to new add image to the repository
    """
    url = "http://localhost:8000/api/images"

    payload = metadata._asdict()
    files = {
        'metadata': (None, json.dumps(payload), 'application/json'),
        'file': (path, open(path, 'rb'), f'image/{metadata.file_type}')
    }
    headers = {
        'Content-Disposition': f'attachment; filename={metadata.name}'
    }

    response = requests.request("POST", url, headers=headers, files=files)
    return response.status_code == 201, response.json()


def search_by_tags(tags: List[str]) -> Tuple[bool, Any]:
    """
    Function for making GET request to search for images to the repository
    based on given list of tags.
    """
    url = f"http://localhost:8000/api/images/tag"

    payload = {'tags': json.dumps(tags)}
    response = requests.request("GET", url, params=payload)
    return response.status_code == 200, response.json()


def search_by_thumbnail(image_hash: str) -> Tuple[bool, Any]:
    url = "http://localhost:8000/api/images/thumbnail"

    payload = {'image_hash': image_hash}
    response = requests.request("GET", url, params=payload)
    return response.status_code == 200, response.json()


def get_image_file(image_id: int, path: str, is_dir: bool) -> Tuple[bool, Any]:
    """
    Function for making GET request to download specific image from the repository.
    """
    url = f"http://localhost:8000/api/images/{image_id}"

    response = requests.request("GET", url)
    if response.status_code != 200:
        return False, response.json()

    header_dis = response.headers['Content-Disposition']
    filename = re.findall("filename=(.+)", header_dis)[0].strip('"')
    save_path = os.path.join(path, filename) if is_dir else path

    with open(save_path, 'wb') as f:
        f.write(response.content)

    return True, save_path
