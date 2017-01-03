
from django.test import TestCase
from django.utils.translation import activate

from api.helper import is_valid_location


class TestView(TestCase):

    def test_i18n(self):
        activate('nb')
        valid, message = is_valid_location("invalid/location")
        activate('ru')
        invalid, invalid_message = is_valid_location("invalid/location")

        self.assertNotEqual(message, invalid_message)
