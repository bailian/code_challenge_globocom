#!/usr/bin/python
# coding: utf-8
from django.conf.urls import url
from bbb.walls import views

app_name = 'wall'

urlpatterns = [
    url(r'^all_votes/(?P<wall_id>\d+)?/?$', views.get_all_votes,
        name='get_all_votes'),
]