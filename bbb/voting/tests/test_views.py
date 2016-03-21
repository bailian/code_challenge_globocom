#/usr/bin/python
# coding: utf-8
from django.core.urlresolvers import reverse
from bbb.core.tests.infrastructure import TestCaseInfrastructure
from bbb.voting.models import Voting


class VotingTests(TestCaseInfrastructure):
    def setUp(self):
        super(VotingTests, self).setUp()

        self.vote = {
            'wall': int(self.wall.pk),
            'vote': int(self.wall.participants.all()[0].pk),
        }

    def test_vote(self):
        response = self.client.post(reverse('voting:voting'), self.vote)
        vote_latest = Voting.objects.latest('pk')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.vote['wall'], vote_latest.wall.pk)
        self.assertEqual(self.vote['vote'], vote_latest.vote.pk)
