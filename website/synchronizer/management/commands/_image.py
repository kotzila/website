import os
from synchronizer.contstans import IMAGE_ORIGINAL_URL
from images.models import Image
from django.conf import settings
import requests


def download_file(url, path=os.path.join(settings.MEDIA_ROOT, Image.src.field.upload_to)):
    name = url.split('/')[-1]
    local_filename = '{}/{}'.format(path, name)

    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    return name

def upload_image(id):
    url = IMAGE_ORIGINAL_URL.format(id)
    image = download_file(url)
    image = '{}/{}'.format(Image.src.field.upload_to, image)
    image = Image(src=image, order=99)
    image.save()
    return image
