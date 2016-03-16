# coding: utf-8
from django.db import models
from bbb.editions.models import Editions
from bbb.participants.models import Participants


class Walls(models.Model):
    edition = models.ForeignKey(Editions, null=False, blank=False)
    participant1 = models.ForeignKey(Participants, null=False, blank=False,
                                     related_name='participant1')
    participant2 = models.ForeignKey(Participants, null=False, blank=False,
                                     related_name='participant2')
    date_finish = models.DateTimeField(u'Data de término', auto_now=False,
                                       auto_now_add=False)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return u'Participantes: %s vs %s' % (self.participant1.name,
                                             self.participant2.name)

    class Meta:
        verbose_name = u'Paredão'
        verbose_name_plural = u'Paredões'
