# Image Repository

## Features

- ADD image(s) to the repository
  - one / bulk / enormous amount of images
  - private or public (permissions)
  - secure uploading and stored images

- SEARCH function
  - from text/description, tags/category
  - from an image (search for similar images) (implement if time permits)
  - from characteristics of the images (implement if time permits)


## Implementation

- An API web server for handling add and search functionality and any future functionality.

- A command line tool for submitting requests to the API server.


## Installation

1. Download or clone the repository
2. Create a virtual environment: `python -m venv env`
3. Activate the virtual environment: `source env/bin/activate`
4. Install the required Python packages: `pip install -r requirements.txt`
5. Create database instance: `python manage.py migrate`

## Usage

Before doing anything, start up Django server: `python manage.py runserver`
so that all the CLI commands can be correctly processed.

To see all the available commands in CLI, run `python main.py --help`

To see details about a specific CLI command, run `python main.py <command> --help`

Here is a list of available operations:
- Add single image
- Add all images in a folder
- Search all images with given list of tags
- Get the specific image from repository using its ID.


## API Endpoints

| Endpoint               | Type | Description          | Body |
|------------------------|------|----------------------|------|
| /api/images            | POST | Add images           |      |
| /api/images/tag        | GET  | Search for images    |      |
| /api/images/{image_id} | GET  | Get a specific image |      |
