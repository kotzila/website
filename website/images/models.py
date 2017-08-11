from django.db import models
from django.db.models.signals import pre_delete
from django.db.models.fields.files import FieldFile
from synchronizer.mixins import TmdbImageSynchronizeMixin


class Image(TmdbImageSynchronizeMixin, models.Model):
    src = models.ImageField(upload_to='p/w', max_length=255)
    iso_639_1 = models.CharField(max_length=2, blank=True)
    order = models.PositiveSmallIntegerField(default=99)

    def __str__(self):
        return self.src.name.split('/')[-1]


def file_cleanup(sender, instance, *args, **kwargs):
    """
    Deletes the file(s) associated with a model instance.
    """
    for field_name in instance.__dict__:
        field = getattr(instance, field_name)
        if issubclass(field.__class__, FieldFile) and field.name:
            field.delete(save=False)


pre_delete.connect(file_cleanup, sender=Image)
