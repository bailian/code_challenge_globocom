#!/usr/bin/python
# coding: utf-8
from django.shortcuts import render
import logging
from bbb.walls.models import Walls

logger = logging.getLogger(__name__)


def get_all_votes(request, wall_id=None):
    msg = None

    if wall_id:
        try:
            wall = Walls.objects.get(pk=wall_id)
        except Walls.DoesNotExist:
            msg = 'Paredão não encontrado.'
            wall = None

        if wall:
            total_votes = len(wall.voting_set.filter(status=True))

    context = {
        'subeditors': 'Todos os votos do paredão',
        'total_votes': total_votes,
        'wall': wall,
        'type_report': 'all_votes',
        'msg': msg,
    }
    return render(request, 'desktop/report.html', context)


def get_all_votes_participant(request, wall=None, participant=None):
    pass


def get_all_votes_per_hours(request, wall=None):
    pass