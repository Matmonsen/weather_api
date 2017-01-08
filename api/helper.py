import datetime
from time import mktime
from typing import List, Tuple
import math
from py_yr.config.settings import LANGUAGE, FORECAST_TYPE_STANDARD, FORECAST_TYPE_HOURLY
from django.utils.translation import ugettext as _
from py_yr.yr import Yr

from api.models import Credit, Time, WindSpeed, WindDirection, Temperature, Symbol, Pressure, Precipitation, Forecast, \
    Location, TimeZone, Sun

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
    if location is None:
        return False, _('InvalidLocation')

    if location.endswith('/'):
        trimmed_location = location[:-1]
    else:
        trimmed_location = location

    params = list(filter(None, trimmed_location.split('/')))
    if not 3 <= len(params) <= 4:
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
    if forecast_type is not None and forecast_type in [FORECAST_TYPE_STANDARD , FORECAST_TYPE_HOURLY]:
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


def save_weather_data(yr_object: Yr) -> Tuple[Forecast, List[Time]]:
    """
        Saves a Yr data object and returns the data

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
    return forecast, times


def time_is_less_then_x_minutes_ago(created: datetime, minutes: datetime) -> bool:
    """
        Determines if a datetime is less then x minutes ago

        Args:
            created (datetime.now): Datetime to check
            minutes (int): Number of minutes

        Examples:
            >>> date_time = datetime.datetime(2015, 8, 18, 20, 21, 44, 799809)
            >>> print(time_is_less_then_x_minutes_ago(date_time, 10))
            False
            >>> print(time_is_less_then_x_minutes_ago(datetime.datetime.now(), 10))
            True

        Returns:
            Bool based on timestamp before or after
    """

    try:
        now = datetime.datetime.now()

        # convert to unix timestamp
        now_ts = mktime(now.timetuple())
        then_ts = mktime(created.timetuple())
        return math.floor(int(then_ts - now_ts) / 60) <= minutes
    except (AttributeError, TypeError) as e:
        return False


def cleanup_response(forecasts, language, forecast_type) -> list:
    """
        Cleans up the forecasts response.
        Some forecasts goes seven days, from monday to monday, so we get double values on that day.
        The actual day, then 7 days ahead.
        Also assorts each forecast to a weekday
        Args:
            forecasts(list): The list containing all of the forecasts.
            language(str): The language of the weather forecast.
            forecast_type(str): The forecast type (hourly/standard)

        Returns(list): List of the weather forecast

        """

    # Generates weekdays based on forecast list
    weekdays = {}
    for forecast in forecasts:
        weekday = DAYS[language][forecast.get('start', '').weekday()]
        try:
            test_if_key_exists = weekdays[weekday]
        except KeyError:
            weekdays[weekday] = {
                'weekday': weekday,
                'forecast': []
            }

    # Add forecast to respective day
    for forecast in forecasts:
        weekday = DAYS[language][forecast.get('start', '').weekday()]
        try:
            weekdays[weekday]['forecast'].append(forecast)
        except KeyError:
            pass

    # Cleans up if some day has more then 4 periods.
    # Typically a if call week on a thursday the 4.
    # Then the thursday will have 6 - 8 fields.
    # With today's date (the 4.) and next week fields 4+7=11.
    # We remove those next week with this method
    if forecast_type is FORECAST_TYPE_STANDARD:
        for i, key in enumerate(weekdays):
            list_of_forecasts = weekdays[key]['forecast']
            if len(list_of_forecasts) > 4:
                # find the smallest date
                lowest_date = datetime.datetime(2100, 12, 12).date()
                for elm in list_of_forecasts:
                    if elm.get('start', lowest_date).date() < lowest_date:
                        lowest_date = elm.get('start', lowest_date).date()

                # copy new with all those dates
                weekdays[key]['forecast'] = [elm for elm in list_of_forecasts if elm.get('start', lowest_date).date() == lowest_date]

    return [weekdays[key] for key in weekdays]