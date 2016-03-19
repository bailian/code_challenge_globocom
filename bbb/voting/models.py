#!/bbb/bin/python
# coding: utf-8
from django.db import models
from bbb.walls.models import Walls
from bbb.participants.models import Participants


class Voting(models.Model):
    wall = models.ForeignKey(Walls)
    vote = models.ForeignKey(Participants)
    date_vote = models.DateTimeField(u'Data do voto', auto_now_add=True)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % self.vote

    class Meta:
        verbose_name = u'Votação'
        verbose_name_plural = u'Votações'
