from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.utils import IntegrityError
import tmdbsimple as tmdb
from common.models import Genre


class Command(BaseCommand):
    help = 'Import genres from tmdb'

    def handle(self, *args, **options):
        tmdb.API_KEY = settings.SECRET_TMDB_API_KEY
        genre_ = tmdb.Genres()

        response = genre_.list()
        genres_list = [Genre(id=item['id'], tmdb_id=item['id'], title=item['name'], title_en=item['name'])
                       for item in response['genres']]

        try:
            Genre.objects.bulk_create(genres_list)
        except IntegrityError:
            print('Genres already exists')
            exit(0)
