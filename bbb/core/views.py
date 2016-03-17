#!/bbb/bin/python
# coding: utf-8
from django.shortcuts import render
from django.core.urlresolvers import reverse
from bbb.participants.models import Participants


def index(request):
    context = {
        'subeditors': 'Participantes',
        'participants': Participants.objects.filter(status=True),
    }
    return render(request, 'desktop/index.html', context)

