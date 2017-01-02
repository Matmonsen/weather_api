from py_yr.config.settings import LANGUAGE, FORECAST_TYPE_STANDARD, FORECAST_TYPE_HOURLY
from django.utils.translation import ugettext as _
from py_yr.yr import Yr

from api.models import Credit, Time, WindSpeed, WindDirection, Temperature, Symbol, Pressure, Precipitation, Forecast, \
    Location, TimeZone

DAYS = {
    'en': [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
    ],
    'nb': [
        'Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Laurdag', 'Søndag',
    ],
    'nn': [
        'Måndag', 'Tysdag', 'Onsdag', 'Torsdag', 'Fredag', 'Laurdag', 'Sundag',
    ],
}


def is_valid_location(location) -> tuple:
    """
    Checks if a location is in the valid format
    Args:
        location (str): Location to be validated

    Returns (tuple): Validation status and invalid message

    """
    if not (location is not None and len(location) > 3 and (
                    len(location.split('/')) is 3 or len(location.split('/'))) is 4):
        return False, _('InvalidLocation')

    return True, ''


def is_valid_language(language) -> tuple:
    """
    Checks if a language is valid
    Args:
        language (str): Language to be validated

    Returns (tuple): Validation status and invalid message

    """
    if language is None or language not in LANGUAGE:
        return False, _('InvalidLanguage')

    return True, ''


def is_valid_forecast_type(forecast_type) -> tuple:
    """
    Checks if a forecast_type is in the valid format
    Args:
        forecast_type (str): Forecast type to be validated

    Returns (tuple): Validation status and invalid message

    """
    if forecast_type is not None and (forecast_type is FORECAST_TYPE_STANDARD or forecast_type is FORECAST_TYPE_HOURLY):
        return True, ''

    return False, _('InvalidForecastType')


def validate_search_request(language, location, forecast_type) -> tuple:
    """
    Checks if a location and a forecast type is in the valid format
    and if the language is supported
    Args:
        language (str): Language to be validated
        location (str): Location to be validated
        forecast_type (str): Forecast type to be validated

    Returns (dict): Validation status and invalid message(s)

    """
    valid_language, language_message = is_valid_language(language)
    valid_location, location_message = is_valid_location(location)
    valid_forecast_type, forecast_type_message = is_valid_forecast_type(forecast_type)

    return valid_language and valid_location and valid_forecast_type, '{0} {1} {2}'.format(
        forecast_type_message,
        location_message,
        language_message)


def save_weather_data(yr_object: Yr) -> None:
    """
        Saves a Yr data object

        Args:
            yr_object (Yr): An yr object containing weather data
    """

    data = yr_object.get_as_object()

    # Location
    timezone = TimeZone(
        utcoffsetMinutes=data.location.timezone.utcoffsetMinutes,
        zone=data.location.timezone.id
    )
    timezone.save()

    location = Location(
        timezone=timezone,
        name=data.location.name,
        country=data.location.country,
        type=data.location.type
    )
    location.save()

    # Sun
    sun = Sun(
        rise=data.sun.rise,
        set=data.sun.set
    )
    sun.save()

    # Credit
    credit = Credit(
        url=data.credit.url,
        text=data.credit.text
    )
    credit.save()

    # Forecast
    forecast = Forecast(
        sun=sun,
        credit=credit,
        location=location,
        search=yr_object.location,
        forecast_type=yr_object.forecast_type,
        language=yr_object.language
    )
    forecast.save()

    # Periods
    times = []
    for t in data.forecast.tabular.time:
        rain = Precipitation(
            value=t.precipitation.value,
        )
        try:
            rain.minValue = t.precipitation.min_value
        except AttributeError:
            pass
        try:
            rain.maxValue = t.precipitation.max_value
        except AttributeError:
            pass
        rain.save()

        pressure = Pressure(
            unit=t.pressure.unit,
            value=t.pressure.value
        )
        pressure.save()

        try:
            temp = t.symbol.var.split('/')[1]
            temp = temp.split('.')[0]
        except IndexError:
            temp = t.symbol.var

        symbol = Symbol(
            name=t.symbol.name,
            var=temp,
            number=t.symbol.number

        )
        symbol.save()

        temp = Temperature(
            unit=t.temperature.unit,
            value=t.temperature.value
        )
        temp.save()

        direction = WindDirection(
            degree=t.windDirection.deg,
            code=t.windDirection.code,
            name=t.windDirection.name
        )
        direction.save()

        speed = WindSpeed(
            mps=t.windSpeed.mps,
            name=t.windSpeed.name
        )
        speed.save()

        time = Time(
            start=t.from_,
            end=t.to,
            period=t.period,
            forecast=forecast,
            precipitation=rain,
            symbol=symbol,
            wind_direction=direction,
            wind_speed=speed,
            temperature=temp,
            pressure=pressure
        )
        time.save()
        times.append(time)