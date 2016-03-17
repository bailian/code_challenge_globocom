#!/bbb/bin/python
# coding: utf-8
from django.db import models
from bbb.editions.models import Editions
from bbb.participants.models import Participants


class Walls(models.Model):
    edition = models.ForeignKey(Editions, null=False, blank=False)
    participants = models.ManyToManyField(Participants)
    date_start = models.DateTimeField(u'Data do início', auto_now_add=True)
    date_finish = models.DateTimeField(u'Data de término', auto_now=False,
                                       auto_now_add=False)
    status = models.BooleanField(default=True)

    def get_participants(self):
        participants = []
        for participant in self.participants.all():
            participants.append(participant)
        return participants

    def __unicode__(self):
        participants = []
        for participant in self.participants.all():
            participants.append(participant.name)
        return u'Participantes: %s' % ','.join(participants)

    class Meta:
        verbose_name = u'Paredão'
        verbose_name_plural = u'Paredões'
