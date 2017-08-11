import logging
from datetime import datetime
from django.conf import settings
from synchronizer.contstans import LANG
from stars.models import Star, SocialIds
import tmdbsimple as tmdb
from pprint import pprint
from ._image import upload_image

logger = logging.getLogger(__name__)


def upload_star_by_tmdb_id(id):
    try:
        Star.objects.get(tmdb_id=id)
        print('Star {} already exists'.format(id))
        # logger.warning('Star {} already exists'.format(id))
        return
    except Star.DoesNotExist:
        pass
    tmdb.API_KEY = settings.SECRET_TMDB_API_KEY
    print('Processing {}'.format(id))

    people = tmdb.People(id)
    response = people.info()
    # check if dates in correct format
    birthday, deathday = response['birthday'], response['deathday']
    if birthday:
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            # wrong format
            birthday = None
    if deathday:
        try:
            datetime.strptime(deathday, '%Y-%m-%d')
        except ValueError:
            deathday = None
    star_dict = {'tmdb_id': response['id'], 'birthday': birthday, 'deathday': deathday,
                 'gender': response['gender'], 'homepage': response.get('homepage'),
                 'biography': response.get('biography'),
                 'name': response['name'], 'place_of_birth': response.get('place_of_birth', '')}

    poster = response.get('profile_path', '')

    star = Star(**star_dict)
    star.save()

    # add social info
    response = people.external_ids()

    social_dict = {'imdb': response.get('imdb_id', ''), 'facebook': response.get('facebook_id', ''),
                   'instagram': response.get('instagram_id', ''), 'twitter': response.get('twitter_id', ''),
                   'freebase': response.get('freebase_id', ''), 'tv_rage': response.get('tv_rage_id', '')}
    social = SocialIds(star=star, **social_dict)
    social.save()

    if poster:
        # upload image
        image = upload_image(poster)
        star.poster = image
        star.save()


    print('{} id uploaded succesfuly'.format(id))
    # logger.info('{} id uploaded succesfuly'.format(id))
