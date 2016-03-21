#!/usr/bin/python
# coding: utf-8
from django.shortcuts import render
import logging
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

    walls = Walls.objects.filter(status=True)


    context = {
        'subeditors': 'Votos do participante nos paredões por hora',
        # 'participant': participant,
        # 'total_votes': total_votes,
        # 'wall': wall,
        'type_report': 'all_votes_participant',
        'msg': msg,
    }
    return render(request, 'desktop/report.html', context)