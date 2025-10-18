import os
from typing import Any, Literal

import requests

QueryField = Literal['zip', 'city']


def get_user_input() -> tuple[QueryField, str]:
    """Takes user input and structures response for GET methods"""
    while True:
        input_choice: str = input('Would you like to get weather information? [y/n]: ')
        if input_choice.lower() == 'y':
            query_field: str = input('Great! Want to fetch by city name or zip code? [city/zip]: ')
        else:
            return 'zip', ''

        if query_field == 'zip':
            return query_field, input('Please enter a zip code: ')
        elif query_field == 'city':
            return query_field, input('Please enter a city name: ')
        else:
            print('Oops, please choose "city" or "zip"!')


def _get_json(query_field: QueryField, query_value: str) -> dict[str, Any]:
    endpoint: str = 'http://api.openweathermap.org/data/2.5/weather'

    params: dict[str, str] = {'zip': f'{query_value},us'} if query_field == 'zip' else {'q': query_value}

    assert (API_KEY := os.getenv('API_KEY')), 'Missing environment variable: API_KEY'
    params['appid'] = API_KEY

    return requests.get(endpoint, params=params).json()


def get_temperature(query_field: QueryField, query_value: str) -> int:
    """Takes structured user input and fetches temperature in Fahrenheit"""
    response: dict[str, Any] = _get_json(query_field, query_value)
    temp_k: float = response['main']['temp']
    temp_f: float = (temp_k - 273.15) * 1.8 + 32

    return int(temp_f)


def get_wind_status(query_field: QueryField, query_value: str) -> str:
    """Takes structured user input and fetches wind status"""
    response: dict[str, Any] = _get_json(query_field, query_value)

    return response['weather'][0]['description']
