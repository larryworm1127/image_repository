from django.db import models


class Tag(models.Model):
    name = models.TextField(primary_key=True, max_length=50)

    def __str__(self):
        return f'Name={self.name}'


class Image(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    description = models.TextField(max_length=200)
    is_public = models.BooleanField()
    url = models.TextField()

    def __str__(self):
        return f'ID={self.pk}, ' \
               f'Desc={self.description}, ' \
               f'Public={self.is_public}, ' \
               f'URL={self.url}'


class ImageTags(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
