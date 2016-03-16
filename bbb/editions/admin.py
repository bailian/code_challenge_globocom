# coding: utf-8
from django.contrib import admin
from bbb.editions.models import Editions


class EditionsAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('edition', 'date_start', 'date_finish', 'status', )
    list_filter = ('status', )


admin.site.register(Editions, EditionsAdmin)
