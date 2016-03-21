#!/usr/bin/python
# coding: utf-8
from django.conf.urls import url
from bbb.walls import views

app_name = 'wall'

urlpatterns = [
    url(r'^relatorio-paredao/(?P<wall_id>\d+)/?$', views.get_all_votes,
        name='get_all_votes'),
    url(
        r'^relatorio-participante/(?P<wall_id>\d+)/(?P<participant_id>\d+)/?$',
        views.get_all_votes_participant, name='get_all_votes_participant'
    ),
    url(r'^relatorio-paredoes-hora/?$', views.get_all_votes_per_hours,
        name='get_all_votes_per_hours'),
]