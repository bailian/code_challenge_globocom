# coding: utf-8
from django.db import models


class Editions(models.Model):
    edition = models.IntegerField(u'Edição', null=False, blank=False)
    description = models.TextField(u'Descrição', null=True, blank=True)
    date_start = models.DateTimeField(u'Data de início', auto_now=False,
                                      auto_now_add=False)
    date_finish = models.DateTimeField(u'Data de término', auto_now=False,
                                       auto_now_add=False)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.edition

    class Meta:
        verbose_name = u'Edição'
        verbose_name_plural = u'Edições'
