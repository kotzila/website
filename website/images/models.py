from django.db import models


class Image(models.Model):
    src = models.ImageField(upload_to='images')
    aspect_ratio = models.FloatField(null=True)
    iso_639_1 = models.CharField(max_length=2, blank=True)
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=99)
