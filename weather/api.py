"""HTTP helpers for interacting with external weather services."""

from __future__ import annotations

import os
from typing import Any

import requests

from .constants import REQUEST_TIMEOUT, WEATHER_ENDPOINT
from .exceptions import WeatherLookupError


def get_api_key() -> str:
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise AssertionError('Missing environment variable: API_KEY')
    return api_key


def request_openweather_json(url: str, params: dict[str, Any] | None = None) -> Any:
    try:
        response: requests.Response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        raise WeatherLookupError('Network error while contacting OpenWeather.') from exc

    try:
        payload: Any = response.json()
    except ValueError as exc:
        raise WeatherLookupError('OpenWeather returned an invalid response.') from exc

    if response.status_code >= 400:
        message: str = payload.get('message') if isinstance(payload, dict) else 'OpenWeather request failed.'
        raise WeatherLookupError(message)

    return payload


def request_zippopotam_json(url: str) -> Any:
    try:
        response: requests.Response = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        raise WeatherLookupError('Network error while contacting Zippopotam.us.') from exc

    if response.status_code >= 400:
        raise WeatherLookupError('Postal code lookup failed.')

    try:
        return response.json()
    except ValueError as exc:
        raise WeatherLookupError('Postal code lookup returned invalid data.') from exc


def fetch_weather(latitude: float, longitude: float, api_key: str) -> dict[str, Any]:
    params: dict[str, Any] = {'lat': latitude, 'lon': longitude, 'appid': api_key}
    payload: Any = request_openweather_json(WEATHER_ENDPOINT, params=params)

    if not isinstance(payload, dict):
        raise WeatherLookupError('Received malformed weather data.')
    return payload
