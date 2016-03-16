# coding: utf-8
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

FILE_SYSTEM = FileSystemStorage(location=settings.MEDIA_ROOT)


def get_upload_to(instance, filename):
    extension = filename.lower().split(".")[-1]
    return 'original/participants/{0}.{1}'.format(
        instance.name.lower(), extension
    )


class Participants(models.Model):
    name = models.CharField(u'Nome', max_length=255, null=False, blank=False)
    codename = models.CharField(u'Apelido', max_length=100, null=True,
                                blank=True)
    description = models.TextField(u'Descrição', null=True, blank=True)
    image = models.ImageField(max_length=255, upload_to=get_upload_to,
                              storage=FILE_SYSTEM, null=False, blank=False)
    status = models.BooleanField(default=True)
