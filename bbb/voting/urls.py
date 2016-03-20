# coding: utf-8
from django.conf.urls import url
from bbb.voting import views

app_name = 'core'

urlpatterns = [
    url(r'^voting/?$', views.voting, name='voting'),
]
