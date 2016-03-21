#!/usr/bin/python
# coding: utf-8
from django.shortcuts import render
import logging
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

    walls = Walls.objects.filter(status=True)
    for wall in walls:
        # vote_per_hours = wall.voting_set.extra({
        #     'date': "EXTRACT(\'day\' FROM \"date_vote\")",
        #     'hour': "EXTRACT(\'hour\' FROM \"date_vote\")"
        # }).values('date', 'hour').order_by('date', 'hour').annotate(Count('id'))
        vote_per_hours = wall.voting_set.extra({
            'date': "DATEPART(\'day\', \"date_vote\")",
            'hour': "DATEPART(\'hour\', \"date_vote\")"
        }).values('date', 'hour').order_by('date', 'hour').annotate(Count('id'))
        print vote_per_hours

    context = {
        'subeditors': 'Votos do participante nos paredões por hora',
        # 'participant': participant,
        # 'total_votes': total_votes,
        # 'wall': wall,
        'type_report': 'all_votes_participant',
        'msg': msg,
    }
    return render(request, 'desktop/report.html', context)