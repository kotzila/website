from __future__ import absolute_import, unicode_literals
import logging
from celery import shared_task
from movies.models import Movie

logger = logging.getLogger(__name__)

@shared_task
def sync_movie_with_tmdb(pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        logger.warning("{} doesn't exists in movie table".format(pk))
        return
    if not movie.tmdb_id:
        logger.warning("{} movie doesn't have tmdb_id".format(movie.pk))
        return

    movie.synchronise_tmdb_releases()
    movie.synchronise_tmdb_videos()
    movie.synchronise_tmdb_images()
    movie.synchronise_tmdb_keywords()
    movie.synchronise_tmdb_credits()
