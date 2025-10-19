"""Shared data structures for weather lookups."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherReport:
    city: str
    zip: str
    temp: int
    status: str

    @property
    def location_label(self) -> str:
        return f'{self.city} ({self.zip})'

    @property
    def wind_description(self) -> str:
        # Backwards compatibility for callers expecting the legacy property.
        return self.status


@dataclass(frozen=True)
class Location:
    city: str
    zip: str
    latitude: float
    longitude: float
