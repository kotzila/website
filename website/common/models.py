from django.db import models


class Genre(models.Model):
    title = models.CharField(max_length=64)
    title_en = models.CharField(max_length=64)
    tmdb_id = models.PositiveSmallIntegerField(null=True)


class KeyWord(models.Model):
    name = models.CharField(max_length=64)
    name_ua = models.CharField(max_length=64, blank=True)
    tmdb_id = models.IntegerField(null=True)


class ProductionCompany(models.Model):
    name = models.CharField(max_length=128)


class Country(models.Model):
    name = models.CharField(max_length=32)
    name_en = models.CharField(max_length=32)
