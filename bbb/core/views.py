#!/bbb/bin/python
# coding: utf-8
from django.shortcuts import render
from django.core.urlresolvers import reverse
from bbb.participants.models import Participants
from bbb.walls.models import Walls
from bbb.voting.forms import VotingForm


def index(request):
    try:
        wall = Walls.objects.get(status=True)
        if not wall.is_open():
            wall = None
    except Walls.DoesNotExist:
        wall = None

    context = {
        'subeditors': 'Participantes',
        'participants': Participants.objects.filter(status=True),
        'wall': wall,
        'form': VotingForm(),
    }
    return render(request, 'desktop/index.html', context)
