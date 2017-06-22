from django.contrib import admin
from images.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('src', 'iso_639_1', 'order')
