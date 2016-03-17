# coding: utf-8
from django.test import TestCase
from StringIO import StringIO
from PIL import Image
from django.core.files.base import File
from bbb.participants.models import Participants


def __create_participant__(name, avatar, codename=None, description=None,
                           status=True):
    return Participants.objects.create(name=name, codename=codename,
                                       image=avatar, status=status)


class TestCaseInfrastructure(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCaseInfrastructure, cls).setUpClass()

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50),
                       color=(256, 0, 0)):
        file_obj = StringIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        self.participants = []

        self.participants.append(__create_participant__(
            'Participante 1', self.get_image_file()))
        self.participants.append(__create_participant__(
            'Participante 2', self.get_image_file()))

    def test_vai(self):
        participant = self.participants[0]
        print participant.name