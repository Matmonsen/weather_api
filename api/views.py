from django.http import HttpRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_exempt
from py_yr.config.settings import LANGUAGE, FORECAST_TYPE_STANDARD, FORECAST_TYPE_HOURLY

from api.helper import validate_search_request


@csrf_exempt
def search(request: HttpRequest) -> JsonResponse:
    """
    Returns weather forecast
    Args:
        request(HttpRequest):

    Returns(JsonResponse): Json response with success, message and data
    """
    language = request.GET.get('language', None)
    location = request.GET.get('location', None)
    forecast_type = request.GET.get('forecastType', None)

    response = {
        'success': False,
        'data': {'meta': None, 'forecasts': None},
        'message': ''
    }
    # Since we get languages in get parameter we have to activate the language manually
    activate(language)

    response['success'], response['message'] = validate_search_request(location, language, forecast_type)
    if not response['success']:
        JsonResponse(response)




    return JsonResponse(response)
