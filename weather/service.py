"""High-level operations exposed to callers."""

from __future__ import annotations

from typing import Any

from .api import fetch_weather, get_api_key
from .exceptions import WeatherLookupError
from .location import resolve_location
from .models import Location, WeatherReport


def get_weather_report(query_value: str) -> WeatherReport:
    """Resolve the query, fetch weather data once, and return a formatted report."""
    api_key: str = get_api_key()
    location: Location = resolve_location(query_value, api_key)
    weather_payload: dict[str, Any] = fetch_weather(location.latitude, location.longitude, api_key)

    main_block: dict[str, Any] = weather_payload.get('main') or {}
    weather_block: list[dict[str, Any]] = weather_payload.get('weather') or []
    if 'temp' not in main_block or not weather_block:
        raise WeatherLookupError('Received incomplete weather information.')

    temp_f: int = kelvin_to_fahrenheit(main_block['temp'])
    description: str = weather_block[0].get('description', 'unavailable')

    return WeatherReport(
        city=location.city,
        zip=location.zip,
        temp=temp_f,
        status=description,
    )


def get_temperature(query_value: str) -> int:
    """Deprecated helper retained for compatibility."""
    return get_weather_report(query_value).temp


def get_wind_status(query_value: str) -> str:
    """Deprecated helper retained for compatibility."""
    return get_weather_report(query_value).wind_description


def kelvin_to_fahrenheit(value: float) -> int:
    temp_f: float = (value - 273.15) * 1.8 + 32
    return int(temp_f)
