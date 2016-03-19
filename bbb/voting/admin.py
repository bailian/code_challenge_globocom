#!/bbb/bin/python
# coding: utf-8
from django.contrib import admin
from bbb.voting.models import Voting


class VotingAdmin(admin.ModelAdmin):
    list_per_page = 12
    list_display = ('wall', 'vote', 'date_vote', 'status', )
    list_filter = ('status', )

admin.site.register(Voting, VotingAdmin)
