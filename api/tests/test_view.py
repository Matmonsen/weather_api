import json

from django.test import Client
from django.test import TestCase
from django.utils.translation import activate

from django.shortcuts import reverse

from py_yr.config.settings import FORECAST_TYPE_STANDARD

from api.helper import is_valid_location


class TestView(TestCase):
    def setUp(self):
        self.location = 'norge/hordaland/bergen/bergen'
        self.language = 'en'
        self.standard = FORECAST_TYPE_STANDARD
        self.hourly = FORECAST_TYPE_STANDARD

        self.client = Client()

    def test_i18n(self):
        activate('nb')
        valid, message = is_valid_location("invalid/location")
        activate('ru')
        invalid, invalid_message = is_valid_location("invalid/location")

        self.assertNotEqual(message, invalid_message)

    def test_valid_standard_search(self):
        response = self.client.get(reverse('search'), {
            'location': self.location,
            'language': self.language,
            'forecastType': self.standard
        })

        self.assertEqual(response.status_code, 200)
        data = json.loads(str(response.content, encoding='utf8'))
        self.assertIsNotNone(data['data']['meta'])
        self.assertIsNotNone(data['data']['forecasts'])
        self.assertTrue(data['success'])

    def test_invalid_location(self):
        response = self.client.get(reverse('search'), {
            'location': 'invalid',
            'language': self.language,
            'forecastType': self.standard
        })

        self.assertEqual(response.status_code, 200)
        data = json.loads(str(response.content, encoding='utf8'))
        self.assertIsNone(data['data']['meta'])
        self.assertIsNone(data['data']['forecasts'])
        self.assertFalse(data['success'])

    def test_invalid_language(self):
        response = self.client.get(reverse('search'), {
            'location': self.location,
            'language': 'invalid',
            'forecastType': self.standard
        })

        self.assertEqual(response.status_code, 200)
        data = json.loads(str(response.content, encoding='utf8'))
        self.assertIsNone(data['data']['meta'])
        self.assertIsNone(data['data']['forecasts'])
        self.assertFalse(data['success'])

    def test_invalid_forecast_type(self):
        response = self.client.get(reverse('search'), {
            'location': self.location,
            'language': self.language,
            'forecastType': 'invalid'
        })

        self.assertEqual(response.status_code, 200)
        data = json.loads(str(response.content, encoding='utf8'))
        self.assertIsNone(data['data']['meta'])
        self.assertIsNone(data['data']['forecasts'])
        self.assertFalse(data['success'])

    def test_all_fields_invalid(self):
        response = self.client.get(reverse('search'), {
            'location': 'invalid',
            'language': 'invalid',
            'forecastType': 'invalid'
        })

        self.assertEqual(response.status_code, 200)
        data = json.loads(str(response.content, encoding='utf8'))
        self.assertIsNone(data['data']['meta'])
        self.assertIsNone(data['data']['forecasts'])
        self.assertFalse(data['success'])
