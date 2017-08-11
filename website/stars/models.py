from django.db import models
from images.models import Image
from helpers.model_mixins import PublishedMixin


class Star(PublishedMixin, models.Model):
    tmdb_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    name = models.CharField(max_length=128)
    name_ua = models.CharField(max_length=128)
    biography = models.TextField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=128, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    deathday = models.DateField(blank=True, null=True)
    gender = models.PositiveSmallIntegerField(blank=True, null=True, help_text='1- female, 2- male')
    homepage = models.URLField(blank=True, null=True)

    poster = models.ForeignKey(Image, blank=True, null=True, help_text='main photo for this star')

    translated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class SocialIds(models.Model):
    star = models.OneToOneField(Star)
    imdb = models.CharField(max_length=64, blank=True, null=True)
    facebook = models.CharField(max_length=64, blank=True, null=True)
    instagram = models.CharField(max_length=64, null=True)
    twitter = models.CharField(max_length=64, blank=True, null=True)
    freebase = models.CharField(max_length=64, blank=True, null=True)
    tv_rage = models.CharField(max_length=64, blank=True, null=True)
