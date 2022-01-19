# Image Repository

## Overview

For the Shopify Developer Intern Challenge, I created an image repository with a CLI client alongside a web API server.
See below for more information.

## Features

- ADD image(s) to the repository
    - one / bulk / enormous amount of images
    - private or public (permissions)
    - duplicate image prevention

- SEARCH function
    - from tags/category
    - from similar image

- GET function
    - download specific image from repository
    - view public image's thumbnail on web browser

## Installation/Setup

1. Download or clone the repository
2. Create a virtual environment: `python -m venv env`
3. Activate the virtual environment: `source env/bin/activate`
4. Install the required Python packages: `pip install -r requirements.txt`
5. Create database instance: `python manage.py migrate`
6. Start up Django server: `python manage.py runserver`

## Usage

Ensure that you are inside the Python virtual environment before running any CLI commands.

To see all the available commands in CLI, run `python main.py --help`

To see details about a specific CLI command, run `python main.py <command> --help`

Here is a list of available operations:

- "add_image": Adds a single image from file system to the repository given all the metadata (or use default)
    - If add image is successful, public images' thumbnail can be viewed
      at: http://127.0.0.1:8000/images/{image_id}.jpeg
    - If user attempts to add a duplicate image, error will be printed
- "add_images": Adds all the image from a folder in the file system to the repository given all the metadata (or use
  default). Concurrency is implemented for faster upload.
- "tag_search": Search all images that contains the list of given tags (returns image metadata instead of actual image)
- "thumbnail_search": Search all images that are similar to a given thumbnail at path in file system (returns image
  metadata instead of actual image)
- "get_image": Download image from repository given an image ID (can be obtained from image metadata)

## Tests

To run all existing tests, run `python manage.py test` under virtual environment

## Implementation

- A Django API web server for handling requests made by user from the CLI client. The web server interacts directly with
  the database and the image storage to perform the following operations:
    - Add image: The server validates and saves a multipart request that consists of a file's byte code and its
      metadata.
    - Search image by tag: The server queries the database and returns a set of images' metadata whose tags matches all
      the ones included in the request parameter.
    - Search similar image: The server queries the database to find images with similar hash value as the image given in
      input.
    - Download image: The server queries the location of the image from database and sends the image to the user.
    - With scalability considered, new server endpoints for new functionalities can be easily added alongside the
      existing ones in the future.

- A command line tool for submitting requests to the API server. See Usage section for more details about the commands

## Future Feature Ideas

- Full text search for image description.
- Add tests for CLI client.
- Make CLI client installable.
- A better image hashing algorithm for searching similar images in the repository.
- Authentication for private/public image.
- Use a cloud storage system (e.g., AWS S3) to store the images instead of storing them in local file system
