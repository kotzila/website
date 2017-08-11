from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from movies.models import Movie, Info, Video, Release, Credit
from movies.forms import MovieForm, VideoForm
from movies.tasks import sync_movie_with_tmdb


class InfoInline(admin.StackedInline):
    model = Info
    exclude = ('popularity', 'vote_average', 'vote_count')


class VideoInline(admin.TabularInline):
    model = Video


class ReleaseInline(admin.TabularInline):
    model = Release


class CreditInline(admin.StackedInline):
    model = Credit


def tmdb_syncrhonise(modeladmin, request, queryset):
    for pk in queryset.values_list('pk', flat=True):
        sync_movie_with_tmdb.delay(pk)

    modeladmin.message_user(request, _('Success'), level=messages.SUCCESS)


tmdb_syncrhonise.short_description = _("Synchronise movies with tmdb")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieForm
    inlines = (InfoInline, VideoInline, ReleaseInline)
    list_display = ('title', 'release_date', 'release_status', 'get_translated')
    list_filter = ('release_status', 'info__translated', 'release_date', 'production_countries')
    search_fields = ('title', )
    actions = [tmdb_syncrhonise]

    def get_translated(self, obj):
        return obj.info.translated


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
