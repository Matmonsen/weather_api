import datetime

from django.http import HttpRequest
from django.http import JsonResponse
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_exempt
from py_yr.yr import Yr

from api.helper import validate_search_request, time_is_less_then_x_minutes_ago, save_weather_data, cleanup_response
from api.models import Forecast, Time


@csrf_exempt
def search(request: HttpRequest) -> JsonResponse:
    """
    Returns weather forecast
    Args:
        request(HttpRequest):

    Returns(JsonResponse): Json response with success, message and data
    """
    response = {
        'success': False,
        'data': {
            'meta': None,
            'forecasts': None
        },
        'message': ''
    }

    # Fetches the get parameters
    language = request.GET.get('language', None)
    location = request.GET.get('location', None)
    forecast_type = request.GET.get('forecastType', None)

    # Since we get languages in get parameter we have to activate the language manually
    activate(language)

    # Validates the get parameters
    response['success'], response['message'] = validate_search_request(language, location, forecast_type)
    if not response['success']:
        return JsonResponse(response)

    # So that the location matches the stored location
    if location[:-1] is not '/':
        location += '/'

    # Fetches the data
    try:
        forecast = Forecast.objects \
            .filter(search=location, language=language, forecast_type=forecast_type) \
            .latest('created')
        # Forecasts is cached and cache is NOT too old
        if time_is_less_then_x_minutes_ago(forecast.created, 10):
            time_list = Time.objects.filter(forecast=forecast.id)
            format_response(response, time_list, forecast, language, forecast_type)
        else:
            # Forecasts is cached, but the cache IS too old
            yr = Yr(location, language, forecast_type)
            yr.download()

            if yr.source_data:
                forecast, time_list = save_weather_data(yr)
                format_response(response, time_list, forecast, language, forecast_type)
            else:
                response['success'] = False
                response['message'] = 'An error occurred'
    except Forecast.DoesNotExist:
        yr = Yr(location, language, forecast_type)
        yr.download()
        if yr.source_data:
            forecast, time_list = save_weather_data(yr)
            format_response(response, time_list, forecast, language, forecast_type)
        else:
            response['success'] = False
            response['message'] = 'An error occurred'

    return JsonResponse(response)


def format_response(response, time_list, forecast, language, forecast_type):
    # format response
    forecasts = [time_data.to_dict() for time_data in time_list]
    response['data']['meta'] = forecast.to_dict()
    response['data']['forecasts'] = cleanup_response(forecasts, language, forecast_type)
    response['data']['lastModified'] = '{0}Z'.format(datetime.datetime.now(), '01')
