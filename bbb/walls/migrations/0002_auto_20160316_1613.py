# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-16 16:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='walls',
            name='participant1',
        ),
        migrations.RemoveField(
            model_name='walls',
            name='participant2',
        ),
    ]