from django.db import models


class Tag(models.Model):
    """
    Model that represents a tag that categorizes the image.
    """
    name = models.TextField(primary_key=True)

    def __str__(self):
        return f'Name={self.name}'


class ImageMetadata(models.Model):
    """
    Model for storing various image metadata.
    """
    image_id = models.BigAutoField(primary_key=True)
    name = models.TextField(max_length=50)
    file_type = models.TextField(max_length=10)
    size = models.IntegerField()
    description = models.TextField(max_length=200, blank=True)
    is_public = models.BooleanField()
    location = models.TextField()
    image_hash = models.TextField(max_length=256, unique=True)

    def __str__(self):
        return (
            f'ID={self.image_id}, '
            f'Name={self.name}, '
            f'Public={self.is_public}, '
            f'Type={self.file_type}, '
            f'Location={self.location}'
        )


class ImageTags(models.Model):
    """
    Model for describing the tag categories that images have.
    """
    image = models.ForeignKey(ImageMetadata, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
