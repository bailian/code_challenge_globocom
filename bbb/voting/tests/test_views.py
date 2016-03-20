#/usr/bin/python
# coding: utf-8
from django.core.urlresolvers import reverse
from bbb.core.tests.infrastructure import TestCaseInfrastructure
from bbb.voting.models import Voting


class VotingTests(TestCaseInfrastructure):
    def setUp(self):
        super(VotingTests, self).setUp()

        self.vote = {
            'wall': self.wall.pk,
            'vote': self.participants[0].pk,
        }

    def test_vote(self):
        response = self.client.post(reverse('voting:vote'), self.vote)
        vote_latest = Voting.objects.latest('pk')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.vote['wall'], vote_latest.wall)
        self.assertEqual(self.vote['vote'], vote_latest.vote)




