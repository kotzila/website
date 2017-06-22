from django.db import models
from helpers.model_mixins import PublishedMixin


class Star(PublishedMixin, models.Model):
    tmdb_id = models.PositiveIntegerField(blank=True, null=True)
    imdb_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)
    name_ua = models.CharField(max_length=128)
    biography = models.TextField(blank=True)
    birthday = models.DateField(blank=True)
    deathday = models.DateField(blank=True)
    gender = models.PositiveSmallIntegerField(blank=True, null=True, help_text='1- female, 2- male')
    homepage = models.URLField(blank=True)

    poster = models.ImageField(upload_to='images', blank=True, help_text='main photo for this star')
