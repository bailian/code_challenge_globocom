#!/bbb/bin/python
# coding: utf-8
from datetime import datetime, timedelta
from bbb.core.tests.infrastructure import TestCaseInfrastructure, \
    __create_wall__
import json


class TestWalls(TestCaseInfrastructure):
    def setUp(self):
        super(TestWalls, self).setUp()

        self.wall_close = __create_wall__(
            self.edition, self.participants,
            (datetime.now() - timedelta(days=2)),
            (datetime.now() - timedelta(days=1))
        )

    def test_get_participants(self):
        participants = self.wall.get_participants()
        self.assertEqual(self.participants, participants)

    def test_wall_open(self):
        wall_open = self.wall.is_open()
        wall_close = self.wall_close.is_open()
        self.assertTrue(wall_open)
        self.assertFalse(wall_close)

    def test_get_time_to_finish(self):
        expected = u'<h3>Faltam <span class="time">3 dias</span> para ' \
                   u'encerrar a votação</span></h3>'
        response = self.wall.get_time_to_finish()
        self.assertEqual(expected, response)

    def test_get_result(self):
        expected = {
            'participants': [],
            'total_votes': 23,
        }
        for participant in self.wall.participants.all():
            if participant.name == 'Participante 1':
                votes = 19
            else:
                votes = 4
            part = {'name': participant.name, 'votes': votes}
            expected['participants'].append(part)
        result = self.wall.get_result()
        self.assertDictEqual(expected, result)
