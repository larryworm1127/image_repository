import json
import os.path
import re
from collections import namedtuple
from typing import List

import requests

__all__ = ['Metadata', 'add_image', 'search_by_tags', 'get_image_file']

UPLOAD_SUCCESS = "Image uploaded successfully!"
DOWNLOAD_SUCCESS = "Image downloaded successfully"

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


def add_image(path: str, metadata: Metadata) -> str:
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
    return response.text if response.status_code != 201 else UPLOAD_SUCCESS


def search_by_tags(tags: List[str]) -> str:
    url = f"http://localhost:8000/api/images/tag"

    payload = json.dumps(tags)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


def get_image_file(image_id: int, path: str, is_dir: bool) -> str:
    url = f"http://localhost:8000/api/images/{image_id}"

    response = requests.request("GET", url)
    if response.status_code != 200:
        return response.text

    header_dis = response.headers['Content-Disposition']
    filename = re.findall("filename=(.+)", header_dis)[0].strip('"')
    save_path = os.path.join(path, filename) if is_dir else path
    print(save_path)
    with open(save_path, 'wb') as f:
        f.write(response.content)

    return DOWNLOAD_SUCCESS
