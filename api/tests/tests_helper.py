import datetime

from django.test import TestCase

# Create your tests here.
from py_yr.config.settings import LANGUAGE, FORECAST_TYPE_STANDARD, FORECAST_TYPE_HOURLY

from api.helper import is_valid_location, is_valid_language, is_valid_forecast_type, time_is_less_then_x_minutes_ago
from api.models import TimeZone, Location, Sun, Credit, Forecast, Precipitation, Pressure, Symbol, Temperature, \
    WindDirection, WindSpeed, Time


class TestHelperValidation(TestCase):
    def setUp(self):
        self.valid_location = 'norway/hordaland/bergen/bergen'
        self.invalid_location_to_few = 'norway/hordaland/'
        self.invalid_location_to_many = 'norway/hordaland/bergen/bergen/bergen'
        self.invalid_location_empty = '///'
        self.invalid_location = ''

        self.valid_language_en = 'en'
        self.valid_language_nb = 'nb'
        self.valid_language_nn = 'nb'
        self.invalid_language = 'ru'

        self.valid_forecast_type_hourly = FORECAST_TYPE_HOURLY
        self.valid_forecast_type_standard = FORECAST_TYPE_STANDARD
        self.invalid_forecast_type_hourly = 'invalid'
        self.invalid_forecast_type_standard = 'invalid'

    def test_is_valid_location(self) -> None:
        self.assertTrue(is_valid_location(self.valid_location)[0])
        self.assertFalse(is_valid_location(self.invalid_location_to_few)[0])
        self.assertFalse(is_valid_location(self.invalid_location_to_many)[0])
        self.assertFalse(is_valid_location(self.invalid_location_empty)[0])
        self.assertFalse(is_valid_location(self.invalid_location)[0])

    def test_is_valid_language(self) -> None:
        self.assertTrue(is_valid_language(self.valid_language_en)[0])
        self.assertTrue(is_valid_language(self.valid_language_nb)[0])
        self.assertTrue(is_valid_language(self.valid_language_nn)[0])
        self.assertFalse(is_valid_language(self.invalid_language)[0])

    def test_is_valid_forecast_type(self) -> None:
        self.assertTrue(is_valid_forecast_type(self.valid_forecast_type_hourly)[0])
        self.assertTrue(is_valid_forecast_type(self.valid_forecast_type_standard)[0])
        self.assertFalse(is_valid_forecast_type(self.invalid_forecast_type_hourly)[0])
        self.assertFalse(is_valid_forecast_type(self.invalid_forecast_type_standard)[0])

    def test_validate_search_request(self) -> None:
        self.assertTrue(is_valid_language(self.valid_language_en)[0]
                        and is_valid_location(self.valid_location)[0]
                        and is_valid_forecast_type(self.valid_forecast_type_hourly)[0])
        self.assertFalse(is_valid_language(self.invalid_language)[0]
                         and is_valid_location(self.valid_location)[0]
                         and is_valid_forecast_type(self.valid_forecast_type_hourly)[0])
        self.assertFalse(is_valid_language(self.valid_language_en)[0]
                         and is_valid_location(self.invalid_location)[0]
                         and is_valid_forecast_type(self.valid_forecast_type_hourly)[0])
        self.assertFalse(is_valid_language(self.valid_language_en)[0]
                         and is_valid_location(self.valid_location)[0]
                         and is_valid_forecast_type(self.invalid_forecast_type_standard)[0])


class TestHelperSaving(TestCase):
    def setUp(self):
        self.timezone = TimeZone(
            utcoffsetMinutes=60,
            zone='utc'
        )

        self.location = Location(
            timezone=self.timezone,
            name='norway/hordaland/bergen/bergen',
            country='Norway',
            type='standard'
        )

        self.sun = Sun(
            rise=datetime.datetime.now(),
            set=datetime.datetime.now()
        )

        self.credit = Credit(
            url='credit url',
            text='much credit'
        )

        self.forecast = Forecast(
            sun=self.sun,
            credit=self.credit,
            location=self.location,
            search='norway/hordaland/bergen/bergen',
            forecast_type='standard',
            language='en'
        )

        self.rain = Precipitation(
            value=2.4,
            min_value=0.0,
            max_value=0.2)

        self.pressure = Pressure(
            unit='hpa',
            value=1024
        )

        self.symbol = Symbol(
            name='sun',
            var='01d',
            number=1

        )

        self.temp = Temperature(
            unit='Celsius',
            value=24
        )

        self.direction = WindDirection(
            degree=137.5,
            code='N',
            name='North'
        )

        self.speed = WindSpeed(
            mps=2,
            name='Breeze'
        )

        self.time = Time(
            start=datetime.datetime.now(),
            end=datetime.datetime.now(),
            period=3,
            forecast=self.forecast,
            precipitation=self.rain,
            symbol=self.symbol,
            wind_direction=self.direction,
            wind_speed=self.speed,
            temperature=self.temp,
            pressure=self.pressure
        )

    def test_save_location(self):
        locations = Location.objects.all()
        self.assertTrue(len(locations) is 0)
        self.timezone.save()
        self.location.timezone = self.timezone
        self.location.save()

        locations = Location.objects.all()
        self.assertFalse(len(locations) is 0)

    def test_save_timezone(self):
        timezones = TimeZone.objects.all()
        self.assertTrue(len(timezones) is 0)
        self.timezone.save()
        timezones = TimeZone.objects.all()
        self.assertFalse(len(timezones) is 0)

    def test_save_sun(self):
        suns = Sun.objects.all()
        self.assertTrue(len(suns) is 0)
        self.sun.save()
        suns = Sun.objects.all()
        self.assertFalse(len(suns) is 0)

    def test_save_credit(self):
        creditz = Credit.objects.all()
        self.assertTrue(len(creditz) is 0)
        self.credit.save()
        creditz = Credit.objects.all()
        self.assertFalse(len(creditz) is 0)

    def test_save_forecast(self):
        pass

    def test_save_rain(self):
        rains = Precipitation.objects.all()
        self.assertTrue(len(rains) is 0)
        self.rain.save()
        rains = Precipitation.objects.all()
        self.assertFalse(len(rains) is 0)

    def test_save_pressure(self):
        pressures = Pressure.objects.all()
        self.assertTrue(len(pressures) is 0)
        self.pressure.save()
        pressures = Pressure.objects.all()
        self.assertFalse(len(pressures) is 0)

    def test_save_temperature(self):
        temperatures = Temperature.objects.all()
        self.assertTrue(len(temperatures) is 0)
        self.temp.save()
        temperatures = Temperature.objects.all()
        self.assertFalse(len(temperatures) is 0)

    def test_save_wind_speed(self):
        speeds = WindSpeed.objects.all()
        self.assertTrue(len(speeds) is 0)
        self.speed.save()
        speeds = WindSpeed.objects.all()
        self.assertFalse(len(speeds) is 0)

    def test_save_wind_direction(self):
        directions = WindDirection.objects.all()
        self.assertTrue(len(directions) is 0)
        self.direction.save()
        directions = WindDirection.objects.all()
        self.assertFalse(len(directions) is 0)

    def test_save_symbol(self):
        symbols = Symbol.objects.all()
        self.assertTrue(len(symbols) is 0)
        self.symbol.save()
        symbols = Symbol.objects.all()
        self.assertFalse(len(symbols) is 0)

    def test_save_time(self):
        times = Time.objects.all()
        self.assertTrue(len(times) is 0)
        self.pressure.save()
        self.rain.save()
        self.temp.save()
        self.speed.save()
        self.direction.save()
        self.symbol.save()
        self.credit.save()
        self.sun.save()

        self.timezone.save()

        self.location.timezone = self.timezone
        self.location.save()

        self.forecast.location = self.location
        self.forecast.credit_id = self.credit.id
        self.forecast.sun_id = self.sun.id
        self.forecast.save()

        self.time.wind_direction_id = self.direction.id
        self.time.symbol_id = self.symbol.id
        self.time.pressure_id = self.pressure.id
        self.time.precipitation_id = self.rain.id
        self.time.wind_speed_id = self.speed.id
        self.time.temperature_id = self.temp.id

        self.time.forecast = self.forecast
        self.time.save()
        times = Time.objects.all()
        self.assertFalse(len(times) is 0)


class TestHelper(TestCase):

    def test_is_younger_then(self):
        self.assertFalse(time_is_less_then_x_minutes_ago(datetime.datetime.now() + datetime.timedelta(days=2), 10))
        self.assertTrue(time_is_less_then_x_minutes_ago(datetime.datetime.now(), 10))
        self.assertFalse(time_is_less_then_x_minutes_ago(datetime.datetime.now(), -10))
        self.assertFalse(time_is_less_then_x_minutes_ago(datetime.datetime.now(), None))
        self.assertFalse(time_is_less_then_x_minutes_ago(datetime.datetime.now(), ''))
