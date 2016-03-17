# coding: utf-8
from django.test import TestCase


class TestCaseInfrastructure(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCaseInfrastructure, cls).setUpClass()

    def setUp(self):
        pass
