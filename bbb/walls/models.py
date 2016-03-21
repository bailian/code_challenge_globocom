#!/bbb/bin/python
# coding: utf-8
from django.db import models
from django.utils import timezone
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

    def is_open(self):
        if self.date_finish > timezone.now():
            return True
        return False

    def convert_timedelta(duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return days, hours, minutes, seconds

    def get_time_to_finish(self):
        if self.is_open():
            elapsedTime = self.date_finish - datetime.now()
            if elapsedTime.days == 0:
                days, hours, minutes, seconds = \
                    self.convert_timedelta(elapsedTime)
                return u'<h3>Faltam <span class="time">%s:%s:%s</span> para ' \
                   u'encerrar a votação</span></h3>' % (hours, minutes, seconds)
            else:
                return u'<h3>Faltam <span class="time">%s dias</span> para ' \
                       u'encerrar a votação</span></h3>' % elapsedTime.days

        return u'<h3>Votação encerrada.</h3>'

    def __unicode__(self):
        participants = []
        for participant in self.participants.all():
            participants.append(participant.name)
        return u'Participantes: %s' % ','.join(participants)

    class Meta:
        verbose_name = u'Paredão'
        verbose_name_plural = u'Paredões'
