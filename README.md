# Image Repository

## Features

- ADD image(s) to the repository
  - one / bulk / enormous amount of images
  - private or public (permissions)
  - secure uploading and stored images

- SEARCH function
  - from text/description, tags/category
  - from an image (search for similar images) (implement if have time)
  - from characteristics of the images (implement if have time)


## Implementation

- An API web server for handling add and search functionality and any future functionality.

- A command line tool for submitting requests to the API server.


## API Endpoints

| Endpoint               | Type | Description          | Body |
|------------------------|------|----------------------|---|
| /api/images            | POST | Add images           |   |
| /api/images/search     | GET  | Search for images    |   |
| /api/images/{image_id} | GET  | Get a specific image |   |
