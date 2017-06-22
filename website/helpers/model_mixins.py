from django.db import models
from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices


class PublishedMixin(StatusModel, TimeStampedModel):
    """
    abstract class that contains logic from
      - TimeStampedModel(created and modified fields)
      - StatusModel - publish and and draft statused and additional manager
                      (https://django-model-utils.readthedocs.io/en/latest/models.html#statusmodel)
    """
    STATUS = Choices('draft', 'published')
    class Meta:
        abstract = True


class PublishedMixin(object):
    published = models.BooleanField(default=False)