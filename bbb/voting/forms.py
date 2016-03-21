#!/usr/bin/python
# coding: utf-8
from django import forms


class VotingForm(forms.Form):
    def __init__(self, wall, *args, **kwargs):
        super(VotingForm, self).__init__(*args, **kwargs)
        if wall:
            self.fields['wall'].initial = wall.pk

    wall = forms.CharField(widget=forms.HiddenInput())
    vote = forms.CharField(widget=forms.HiddenInput())
