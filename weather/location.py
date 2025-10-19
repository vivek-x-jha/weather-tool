"""Logic for turning user queries into concrete locations."""

from __future__ import annotations

from typing import Any

from .api import request_openweather_json, request_zippopotam_json
from .constants import (
    GEO_DIRECT_ENDPOINT,
    GEO_ZIP_ENDPOINT,
    US_STATE_ABBREVIATIONS,
    ZIPPOTAM_ENDPOINT,
)
from .exceptions import WeatherLookupError
from .models import Location


def resolve_location(query: str, api_key: str) -> Location:
    normalized_query: str = query.strip()
    if not normalized_query:
        raise WeatherLookupError('No query provided.')

    if looks_like_zip(normalized_query):
        return lookup_location_by_zip(normalized_query, api_key)

    return lookup_location_by_city(normalized_query, api_key)


def looks_like_zip(value: str) -> bool:
    digits_only: str = value.replace('-', '')
    return digits_only.isdigit() and 4 <= len(digits_only) <= 10


def lookup_location_by_zip(zip_code: str, api_key: str) -> Location:
    digits_only: str = zip_code.replace('-', '')
    params: dict[str, str] = {'zip': f'{digits_only},US', 'appid': api_key}
    payload_any: Any = request_openweather_json(GEO_ZIP_ENDPOINT, params=params)
    if not isinstance(payload_any, dict):
        raise WeatherLookupError(f'Unable to resolve ZIP code "{zip_code}".')
    payload: dict[str, Any] = payload_any

    if 'zip' not in payload or 'name' not in payload:
        raise WeatherLookupError(f'Unable to resolve ZIP code "{zip_code}".')

    return Location(
        city=payload['name'],
        zip=payload['zip'],
        latitude=payload['lat'],
        longitude=payload['lon'],
    )


def lookup_location_by_city(city_query: str, api_key: str) -> Location:
    params: dict[str, Any] = {'q': city_query, 'limit': 1, 'appid': api_key}
    payload: Any = request_openweather_json(GEO_DIRECT_ENDPOINT, params=params)

    if not isinstance(payload, list) or not payload:
        raise WeatherLookupError(f'Unable to resolve city "{city_query}".')

    candidate: dict[str, Any] = payload[0]
    city_name: str = candidate.get('name') or city_query
    latitude: float = candidate.get('lat')
    longitude: float = candidate.get('lon')
    if latitude is None or longitude is None:
        raise WeatherLookupError(f'Incomplete location data for "{city_name}".')

    country_code: str = (candidate.get('country') or 'US').upper()
    state_name: str | None = candidate.get('state')
    zip_code: str = lookup_zip_for_city(city_name, country_code, state_name)

    return Location(
        city=city_name,
        zip=zip_code,
        latitude=latitude,
        longitude=longitude,
    )


def lookup_zip_for_city(city_name: str, country_code: str, state_name: str | None) -> str:
    if country_code == 'US':
        state_code: str | None = normalize_state_code(state_name)
        if state_code:
            return lookup_us_zip(city_name, state_code)
        raise WeatherLookupError(f'Unable to determine state for "{city_name}", cannot determine ZIP code.')

    endpoint: str = f'{ZIPPOTAM_ENDPOINT}/{country_code.lower()}/{city_name}'
    payload: Any = request_zippopotam_json(endpoint)
    if isinstance(payload, dict):
        places: Any = payload.get('places')
        if isinstance(places, list) and places:
            entry: dict[str, Any] = places[0]
            zip_candidate: str | None = entry.get('post code') or entry.get('postcode')
            if zip_candidate:
                return zip_candidate

    raise WeatherLookupError(f'Unable to determine postal code for "{city_name}".')


def lookup_us_zip(city_name: str, state_code: str) -> str:
    endpoint: str = f'{ZIPPOTAM_ENDPOINT}/us/{state_code}/{city_name}'
    payload: Any = request_zippopotam_json(endpoint)
    if not isinstance(payload, dict):
        raise WeatherLookupError(f'Unrecognized response when looking up ZIP for "{city_name}, {state_code}".')

    places: Any = payload.get('places')
    if not isinstance(places, list) or not places:
        raise WeatherLookupError(f'No ZIP codes found for "{city_name}, {state_code}".')

    entry: dict[str, Any] = places[0]
    zip_candidate: str | None = entry.get('post code') or entry.get('postcode')
    if not zip_candidate:
        raise WeatherLookupError(f'ZIP code missing from lookup result for "{city_name}, {state_code}".')

    return zip_candidate


def normalize_state_code(state_name: str | None) -> str | None:
    if not state_name:
        return None
    cleaned: str = state_name.strip()
    if len(cleaned) == 2 and cleaned.isalpha():
        return cleaned.upper()

    return US_STATE_ABBREVIATIONS.get(cleaned.lower())
