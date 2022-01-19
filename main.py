"""
Main entry point to the CLI client.
"""
import fire

from cli_client.cli import (
    add_single_image,
    add_multiple_images,
    tag_search,
    get_image,
    thumbnail_search
)

if __name__ == '__main__':
    fire.Fire({
        'add_image': add_single_image,
        'add_images': add_multiple_images,
        'tag_search': tag_search,
        'thumbnail_search': thumbnail_search,
        'get_image': get_image
    })
