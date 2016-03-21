#!/bbb/bin/python
# coding: utf-8
from django.db import models
from django.utils import timezone
from datetime import datetime
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
            elapsedTime = self.date_finish - timezone.now()
            if elapsedTime.days == 0:
                days, hours, minutes, seconds = \
                    self.convert_timedelta(elapsedTime)
                return u'<div><span>Faltam</span><span class="time">' \
                       u'%s:%s:%s</span><span> para encerrar a votação' \
                       u'</span></div>' % (hours, minutes, seconds)
            else:
                if elapsedTime.days == 1:
                    txt_days = u'dia'
                else:
                    txt_days = u'dias'
                return u'<div><span>Faltam</span><span class="time">' \
                       u'%s %s</span><span>para encerrar a votação' \
                       u'</span></div>' % (elapsedTime.days, txt_days)

        return u'<div>Votação encerrada.</div>'

    def get_result(self):
        result = {
            'participants': [],
            'total_votes': 0,
        }

        for participant in self.participants.all():
            votes = self.voting_set.filter(wall=self.pk, vote=participant,
                                          status=True)
            result['participants'].append(
                {'name': participant.name, 'votes': len(votes)}
            )
        result['total_votes'] = len(
            self.voting_set.filter(wall=self.pk, status=True)
        )
        return result

    def __unicode__(self):
        participants = []
        for participant in self.participants.all():
            participants.append(participant.name)
        return u'Participantes: %s' % ','.join(participants)

    class Meta:
        verbose_name = u'Paredão'
        verbose_name_plural = u'Paredões'
