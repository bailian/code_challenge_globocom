#!/bbb/bin/python
# coding: utf-8
from django import forms
from bbb.voting.models import Voting


class VotingForm(forms.Form):
    wall = forms.HiddenInput()
    vote = forms.HiddenInput()

    class Meta:
        model = Voting
