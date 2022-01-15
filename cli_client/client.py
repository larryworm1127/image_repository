import json
from collections import namedtuple

import requests

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


def add_image(path: str, metadata: Metadata):
    url = "http://localhost:8000/api/images"

    payload = metadata._asdict()
    print(payload)
    files = [
        (
            'metadata', (None, json.dumps(payload), 'application/json')
        ),
        (
            'file', (path, open(path, 'rb'), f'image/{metadata.file_type}')
        )
    ]
    headers = {
        'Content-Disposition': f'attachment; filename={metadata.name}'
    }

    response = requests.request("POST", url, headers=headers, files=files)
    print(response.status_code)
    if response.status_code != 201:
        return False, response.text
    return True, "Image uploaded successfully!"
