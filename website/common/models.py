from django.db import models


class Genre(models.Model):
    title = models.CharField(max_length=64)
    title_en = models.CharField(max_length=64)
    tmdb_id = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.title


class KeyWord(models.Model):
    name = models.CharField(max_length=64)
    name_ua = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name


class ProductionCompany(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=32)
    name_en = models.CharField(max_length=32, blank=True)
    iso_3166_1 = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.name
