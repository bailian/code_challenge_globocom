#!/usr/bin/python
# coding: utf-8
from django.http import HttpResponse
from bbb.voting.forms import VotingForm
from bbb.voting.models import Voting
from bbb.walls.models import Walls
from bbb.participants.models import Participants
import logging, json

logger = logging.getLogger(__name__)


def voting(request):
    msg = None
    vote = None
    status = False

    try:
        wall = Walls.objects.get(status=True)
        if not wall.is_open():
            wall = None
    except Walls.DoesNotExist:
        wall = None

    if request.method == 'POST':
        form = VotingForm(wall, request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                vote = Participants.objects.get(pk=int(data['vote']))
            except Participants.DoesNotExist:
                msg = 'Participante não encontrado.'
                log = 'Falha ao buscar o participante com  o id: %s no ' \
                      'paredão: %s.' % (int(data['vote']), wall.pk)
                logger.error(log)
            if vote:
                try:
                    voting = Voting(
                        wall=wall,
                        vote=vote,
                    )
                    voting.save()
                    status = True
                    msg = 'Voto cadastrado com sucesso.'
                except Exception as e:
                    status = False
                    msg = 'Falha ao salvar o voto. Por favor, ente mais tarde.'
                    log = 'Falha na tentativa de efetuar o voto no participante ' \
                          'com  o id: %s no paredão: %s. Error: %s' \
                          % (request.POST['vote'], request.POST['wall'], e)
                    logger.error(log)

    response = {
        'msg': msg,
        'participant': vote,
        'status': status,
    }
    return HttpResponse(json.dumps(response), 'application/json')
