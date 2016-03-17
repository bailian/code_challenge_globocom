#!/bbb/bin/python
# coding: utf-8
from bbb.core.tests.infrastructure import TestCaseInfrastructure


class TestWalls(TestCaseInfrastructure):
    def setUp(self):
        super(TestWalls, self).setUp()

    def test_get_participants(self):
        participants = self.wall.get_participants()
        self.assertEqual(self.participants, participants)
