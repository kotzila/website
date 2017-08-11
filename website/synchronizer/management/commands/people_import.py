import logging
from django.core.management.base import BaseCommand
from django.conf import settings
import tmdbsimple as tmdb
from ._star import upload_star_by_tmdb_id

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import popular people from tmdb'

    def add_arguments(self, parser):
        parser.add_argument('start', type=int, nargs='?', default=1)

    def handle(self, *args, **options):
        tmdb.API_KEY = settings.SECRET_TMDB_API_KEY
        people = tmdb.People()

        curr_page = options['start']
        response = people.popular(page=curr_page)
        total_pages = response['total_pages']

        while curr_page <= total_pages:
            # logger.info('Start processing {} page'.format(curr_page))
            print('Start processing {} page'.format(curr_page))
            response = people.popular(page=curr_page)

            ids = [item['id'] for item in response['results']]
            for id in ids:
                upload_star_by_tmdb_id(id)
            curr_page += 1
