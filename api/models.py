from django.db import models


class Tag(models.Model):
    name = models.TextField(primary_key=True, max_length=50)

    def __str__(self):
        return f'Name={self.name}'


class ImageMetadata(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    name = models.TextField(max_length=50)
    file_type = models.TextField(max_length=10)
    size = models.IntegerField()
    description = models.TextField(max_length=200)
    is_public = models.BooleanField()
    location = models.TextField()

    def __str__(self):
        return f'ID={self.image_id}, ' \
               f'Desc={self.name}, ' \
               f'Public={self.is_public}, ' \
               f'Type={self.file_type}, ' \
               f'Location={self.location}'


class ImageTags(models.Model):
    image = models.ForeignKey(ImageMetadata, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
