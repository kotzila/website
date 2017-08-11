import os
import requests
import tmdbsimple as tmdb
from django.conf import settings
from synchronizer.contstans import IMAGE_ORIGINAL_URL, LANG
from common.models import KeyWord


class TmdbImageSynchronizeMixin(object):
    @classmethod
    def _download_file(cls, url):
        path = os.path.join(settings.MEDIA_ROOT, cls.src.field.upload_to)
        name = url.split('/')[-1]

        local_filename = '{}/{}'.format(path, name)

        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        return name

    @classmethod
    def upload_image_from_tmdb(cls, tmdb_id):
        url = IMAGE_ORIGINAL_URL.format(tmdb_id)
        image = cls._download_file(url)
        image = '{}/{}'.format(cls.src.field.upload_to, image)
        image = cls(src=image, order=99)
        image.save()
        return image


class TmdbMovieSynchronizeMixin(object):
    def synchronise_tmdb_releases(self):
        """
        add ukrainian release if it exists in tmdb
        """
        from movies.models import Release
        tmdb_movie = tmdb.Movies(self.tmdb_id)

        ua_release = [item for item in tmdb_movie.releases()['countries'] if item['iso_3166_1'] == 'UA']
        if ua_release:
            ua_release = ua_release[0]
            Release.objects.create(movie=self, release_date=ua_release['release_date'],
                                   iso_3166_1=ua_release['iso_3166_1'],
                                   certification=ua_release['certification']
                                   )
        return self

    def synchronise_tmdb_videos(self):
        """
        add english and ukrainian videos from tmdb
        """
        from movies.models import Video
        tmdb_movie = tmdb.Movies(self.tmdb_id)

        tmdb_videos = tmdb_movie.videos()['results']

        for item in tmdb_videos:
            if item['iso_639_1'] == 'en' or item['iso_639_1'] == LANG:
                Video.objects.create(movie=self, iso_3166_1=item['iso_3166_1'], iso_639_1=item['iso_639_1'],
                                     key=item['key'], site=item['site'], type=item['type'], size=item['size'])
        return self

    def synchronise_tmdb_images(self):
        """
        add ukrainian images if it exists in tmdb
        """
        from images.models import Image
        tmdb_movie = tmdb.Movies(self.tmdb_id)
        images = tmdb_movie.images()
        images_ids = []
        poster = False
        for item in images['posters']:
            if item['iso_639_1'] == LANG:
                image = Image.upload_image_from_tmdb(item['file_path'])
                # make a poster if exists at least one language specific image
                if not poster:
                    self.poster = image
                    self.save()
                images_ids.append(image.id)
        self.images.add(*images_ids)
        return self

    def synchronise_tmdb_keywords(self):
        """
        synchronise keywords from tmdb
        :return:
        """
        tmdb_movie = tmdb.Movies(self.tmdb_id)
        tmdb_movie.keywords()
        keyword_ids = []
        for item in tmdb_movie.keywords:
            try:
                keyword = KeyWord.objects.get(id=item['id'])
            except KeyWord.DoesNotExist:
                keyword = KeyWord.objects.create(id=item['id'], name=item['name'])
            keyword_ids.append(keyword.id)
        self.keywords.add(*keyword_ids)

    def synchronise_tmdb_credits(self):
        from movies.models import Credit
        from stars.models import Star
        tmdb_movie = tmdb.Movies(self.tmdb_id)
        credits = tmdb_movie.credits()

        credit_objects = []

        for item in credits['cast']:

            item_data = {'status': 'cast', 'movie_id': self.id, 'order': item['order'],
                         'character': item['character'], 'cast_id': item['cast_id'],
                         'tmdb_credit_id': item['credit_id']}
            try:
                star = Star.objects.get(tmdb_id=item['id'])
                item_data['star_id'] = star.id
            except Star.DoesNotExist:
                pass
            credit_objects.append(Credit(**item_data))

        for item in credits['crew']:
            item_data = {'status': 'crew', 'movie_id': self.id,
                         'department': item['department'], 'job': item['job'],
                         'tmdb_credit_id': item['credit_id']}
            try:
                star = Star.objects.get(tmdb_id=item['id'])
                item_data['star_id'] = star.id
            except Star.DoesNotExist:
                pass
            credit_objects.append(Credit(**item_data))

        Credit.objects.bulk_create(credit_objects)
