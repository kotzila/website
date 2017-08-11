from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from requests.exceptions import HTTPError
import tmdbsimple as tmdb
from synchronizer.contstans import LANG
from images.models import Image

tmdb.API_KEY = settings.SECRET_TMDB_API_KEY

from movies.models import Movie, Info, Release, Video
from common.models import ProductionCompany, Country, KeyWord



def handle_info(tmdb_id):
    """
    add information about movie from tmdb to database
    information only from tmdb_movie.info() request
    :param tmdb_id: id from tmdb
    :return: Movie object
    """
    tmdb_movie = tmdb.Movies(tmdb_id)
    try:
        response = tmdb_movie.info(language=LANG)
    except HTTPError as e:
        print(e)
        return
    if len(response['title']) > 128:
        return
    # add main movie data
    main_data = {'title': response['title'], 'release_date': response['release_date'],
                 'release_status': response['status'],
                 'tmdb_id': response['id']}
    movie = Movie(**main_data)
    movie.save()

    info_data = {'original_title': response['original_title'], 'budget': response['budget'],
                 'revenue': response['revenue'], 'homepage': response['homepage'],
                 'original_language': response['original_language'], 'runtime': response['runtime'],
                 'imdb_id': response['imdb_id'], 'overview_ua': response['overview'], 'tagline': response['tagline'],
                 'translated': False}
    if info_data['overview_ua']:
        info_data['overview'], info_data['translated'] = info_data['overview_ua'], True
    else:
        # additional query
        response = tmdb_movie.info()
        info_data['overview'], info_data['tagline'] = response['overview'], response['tagline']
    info = Info(movie=movie, **info_data)
    info.save()

    genres_ids = [item['id'] for item in response['genres']]
    movie.genres.add(*genres_ids)

    # add production companies
    companies_ids = []
    for item in response['production_companies']:
        try:
            company = ProductionCompany.objects.get(id=item['id'])
        except ProductionCompany.DoesNotExist:
            company = ProductionCompany.objects.create(name=item['name'], id=item['id'])

        companies_ids.append(company.id)
    movie.production_companies.add(*companies_ids)

    # add countries
    countries_ids = []
    for item in response['production_countries']:
        try:
            country = Country.objects.get(iso_3166_1=item['iso_3166_1'])
        except Country.DoesNotExist:
            country = Country.objects.create(name=item['name'], iso_3166_1=item['iso_3166_1'])
        countries_ids.append(country.id)
    movie.production_countries.add(*countries_ids)

    # main poster (english)
    poster = response.get('poster_path', '')
    if poster:
        image = Image.upload_image_from_tmdb(poster)
        movie.poster = image
        movie.save()
        movie.images.add(*[image.id])

    return movie


def handle_credits(movie):
    return movie


def upload_movie(tmdb_id):
    print(tmdb_id)
    try:
        Movie.objects.get(tmdb_id=tmdb_id)
        print('Movie {} already exists'.format(tmdb_id))
        # logger.warning('Star {} already exists'.format(id))
        return
    except Movie.DoesNotExist:
        pass

    print('Processing {}'.format(tmdb_id))
    movie = handle_info(tmdb_id)
    if not movie:
        return
    movie.synchronise_tmdb_releases()
    movie.synchronise_tmdb_videos()
    movie.synchronise_tmdb_images()
    movie.synchronise_tmdb_keywords()
    movie.synchronise_tmdb_credits()

    print('{} id uploaded succesfuly'.format(tmdb_id))


# ./manage.py import_movies 2017 3
# where "2017" is primary_release_year and "3" page from which to start processing
class Command(BaseCommand):
    help = 'Import movies from tmdb'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)
    def add_arguments(self, parser):
        parser.add_argument('year', type=int, nargs='?', default=2017)
        parser.add_argument('page', type=int, nargs='?', default=1)
        parser.add_argument('percentage', type=int, nargs='?', default=30)

    def handle(self, *args, **options):
        year, curr_page, percentage = options['year'], options['page'], options['percentage']
        discover = tmdb.Discover()

        response = discover.movie(primary_release_year=year, page=curr_page)
        total_pages = response['total_pages']
        needed_pages = int(total_pages * percentage / 100)

        print('Going tot process {} pages(Total: {})'.format(needed_pages, total_pages))
        while curr_page <= needed_pages:

            print('####################### {} page ########################'.format(curr_page))
            response = discover.movie(primary_release_year=year, page=curr_page)

            ids = [item['id'] for item in response['results']]

            for id in ids:
                upload_movie(id)
            curr_page += 1

        # movie_id = 321612
        # # movie_id = 257368
        # upload_movie(movie_id)
