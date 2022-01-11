from django.db import models


class Tag(models.Model):
    name = models.TextField(primary_key=True, max_length=50)


class Image(models.Model):
    image_id = models.IntegerField(primary_key=True, auto_created=True)
    description = models.TextField(max_length=200)
    is_public = models.BooleanField()
    url = models.TextField()
    tag = models.ManyToManyField(
        Tag,
        through='ImageTags',
        through_fields=('image', 'tag')
    )


class ImageTags(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
