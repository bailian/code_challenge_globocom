#!/usr/bin/python
# coding: utf-8
from django.shortcuts import render
import logging
from datetime import datetime
from django.db.models import Count
from bbb.walls.models import Walls

logger = logging.getLogger(__name__)


def get_all_votes(request, wall_id=None):
    msg = None
    total_votes = 0
    wall = None

    if wall_id:
        try:
            wall = Walls.objects.get(pk=wall_id)
        except Walls.DoesNotExist:
            msg = 'Paredão não encontrado.'

        if wall:
            total_votes = wall.voting_set.filter(status=True).count()

    context = {
        'subeditors': 'Todos os votos do paredão',
        'total_votes': total_votes,
        'wall': wall,
        'type_report': 'all_votes',
        'msg': msg,
    }
    return render(request, 'desktop/report.html', context)


def get_all_votes_participant(request, wall_id=None, participant_id=None):
    msg = None
    participant = None
    total_votes = 0
    wall = None

    if wall_id:
        try:
            wall = Walls.objects.get(pk=wall_id)
        except Walls.DoesNotExist:
            msg = 'Paredão não encontrado.'

    if participant_id and wall:
        votes = wall.voting_set.filter(vote=participant_id, status=True)
        total_votes = len(votes)
        if total_votes > 0:
            participant = votes[0].vote.name
        else:
            msg = "Não existe voto para o participante."

    context = {
        'subeditors': 'Votos do participante no paredão',
        'participant': participant,
        'total_votes': total_votes,
        'wall': wall,
        'type_report': 'all_votes_participant',
        'msg': msg,
    }
    return render(request, 'desktop/report.html', context)


def get_all_votes_per_hours(request):
    msg = None
    result_walls = {'walls': []}

    walls = Walls.objects.filter(edition__status=True)
    for wall in walls:
        vote_per_date = wall.voting_set.all().order_by('date_vote')
        day = None
        for vote_date in vote_per_date:
            if vote_date.date_vote.strftime('%Y-%m-%d') != day:
                for hour_num in range(0, 23):
                    day_hour_start = datetime(
                        vote_date.date_vote.year, vote_date.date_vote.month,
                        vote_date.date_vote.day, hour_num, 00, 00,
                         480538,
                    )
                    day_hour_finish = datetime(
                        vote_date.date_vote.year, vote_date.date_vote.month,
                        vote_date.date_vote.day, hour_num, 59, 00,
                        480538,
                    )

                    all_day = vote_per_date.filter(
                        date_vote__gte=day_hour_start,
                        date_vote__lte=day_hour_finish
                    )
                    if len(all_day) > 0:
                        dates = []
                        str_hour = hour_num
                        if hour_num < 10:
                            str_hour = '0%s' % hour_num
                        hour = {
                            'date':
                                vote_date.date_vote.strftime('%d/%m/%Y'),
                            'hour': '%s:00' % str_hour,
                            'participants': []
                        }

                        for participant in wall.participants.all():
                            hour['participants'].append(
                                {'name': participant.name,
                                 'votes':
                                     all_day.filter(vote=participant).count()
                                 })
                        dates.append(hour)

                        wall_dict = {
                            'wall': wall,
                            'dates': dates
                        }
                        result_walls['walls'].append(wall_dict)
                day = vote_date.date_vote.strftime('%Y-%m-%d')

    context = {
        'subeditors': 'Votos dos participantes nos paredões por hora',
        'walls': result_walls,
        'type_report': 'all_votes_participant_per_hour',
        'msg': msg,
    }
    return render(request, 'desktop/report.html', context)
