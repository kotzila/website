from django.contrib import admin
from movies.models import Movie, Info, Video, Release, Credit


class InfoInline(admin.StackedInline):
    model = Info
    exclude = ('popularity', 'vote_average', 'vote_count')


class VideoInline(admin.TabularInline):
    model = Video

class ReleaseInline(admin.TabularInline):
    model = Release

class CreditInline(admin.StackedInline):
    model = Credit


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = (InfoInline, VideoInline, ReleaseInline, CreditInline)
    filter_horizontal = ('genres', 'images', 'production_companies', 'production_countries', 'keywords')
