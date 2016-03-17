# coding: utf-8
from django.conf.urls import url
from bbb.core import views

app_name = 'core'

urlpatterns = [
    url(r'^index/?$', views.index, name='index'),
    url(r'^', views.index, name='index'),
]
