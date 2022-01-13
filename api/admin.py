from django.contrib import admin

from api.models import ImageMetadata, Tag, ImageTags

admin.site.register(ImageMetadata)
admin.site.register(Tag)
admin.site.register(ImageTags)
