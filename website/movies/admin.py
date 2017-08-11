from django.contrib import admin
from movies.models import Movie, Info, Video, Release, Credit
from movies.forms import MovieForm


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
    form = MovieForm
    inlines = (InfoInline, VideoInline, ReleaseInline)
    list_display = ('title', 'release_status',)
    list_filter = ('release_status', )


from .forms import VideoForm


class VideoAdmin(admin.ModelAdmin):
    form = VideoForm

admin.site.register(Video, VideoAdmin)
