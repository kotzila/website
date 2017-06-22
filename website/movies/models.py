# todo: check max length in all CharFields
from django.db import models
from model_utils import Choices
from model_utils.models import StatusModel
from common.models import Genre, ProductionCompany, Country, KeyWord
from stars.models import Star
from images.models import Image
from helpers.model_mixins import PublishedMixin


class Movie(PublishedMixin, models.Model):
    title = models.CharField(max_length=128, help_text='Main title which will be shoved on website')
    # todo: create something like EnumField or create different table for this field(in last case use index)
    release_status = models.CharField(max_length=16)
    release_date = models.DateField(blank=True)

    poster = models.ForeignKey(Image, blank=True, null=True,
                               on_delete=models.CASCADE,
                               help_text='main poster for this movie',
                               related_name='movie_poster')
    images = models.ManyToManyField(Image, blank=True, null=True, related_name='movie_image')
    genres = models.ManyToManyField(Genre)
    production_companies = models.ManyToManyField(ProductionCompany, blank=True)
    production_countries = models.ManyToManyField(Country)
    keywords = models.ManyToManyField(KeyWord, blank=True)


class Info(models.Model):
    """
    information about movie
    """
    movie = models.OneToOneField(Movie, primary_key=True, on_delete=models.CASCADE)
    original_title = models.CharField(max_length=128, blank=True, help_text='Title in original language')
    title_ua = models.CharField(max_length=128, blank=True)
    title_ru = models.CharField(max_length=128, blank=True)
    overview = models.TextField(blank=True)
    overview_ua = models.TextField(blank=True)

    tagline = models.CharField(max_length=255, blank=True)
    tmdb_id = models.PositiveIntegerField(blank=True, null=True)
    budget = models.PositiveIntegerField(null=True, blank=True, help_text='Total budget in dollars')
    revenue = models.PositiveIntegerField(null=True, blank=True, help_text='Total revenue in dollars')
    revenue_ua = models.PositiveIntegerField(null=True, blank=True, help_text='Revenue in Ukraine')
    homepage = models.URLField(blank=True)
    original_language = models.CharField(max_length=2, blank=True)
    runtime = models.PositiveIntegerField(blank=True, null=True, help_text='Runtime in minutes')

    imdb_id = models.CharField(max_length=16, blank=True)
    tmdb_popularity = models.FloatField(blank=True, null=True, help_text='Popularity in themoviedb')
    popularity = models.FloatField(blank=True, null=True, help_text='Populatity in this website')

    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.PositiveIntegerField(blank=True)


class Video(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    iso_3166_1 = models.CharField(max_length=2)
    iso_639_1 = models.CharField(max_length=2)
    key = models.CharField(max_length=32)
    site = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
    size = models.PositiveIntegerField(blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=999)


class Release(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    release_date = models.DateField()
    certification = models.CharField(max_length=16, help_text='different countries have differrent certification')
    iso_3166_1 = models.CharField(max_length=2)


class Credit(StatusModel, models.Model):
    STATUS = Choices('crew', 'cast')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    star = models.ForeignKey(Star)
    # crew info
    department = models.CharField(max_length=64, blank=True)
    job = models.CharField(max_length=64, blank=True)
    # cast info
    character = models.CharField(max_length=128, blank=True)
    cast_id = models.PositiveIntegerField(blank=True, null=True, help_text='number of role in a movie')

    tmdb_credit_id = models.CharField(max_length=24, unique=True)
    order = models.PositiveSmallIntegerField(default=999)
