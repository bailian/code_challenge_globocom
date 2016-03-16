# coding: utf-8
from django.contrib import admin
from bbb.participants.models import Participants


class ParticipantsAdmin(admin.ModelAdmin):
    list_per_page = 12
    list_display = ('name', 'codename', 'status', )
    list_filter = ('status', )

admin.site.register(Participants, ParticipantsAdmin)
