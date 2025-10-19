"""Exceptions specific to the weather package."""


class WeatherLookupError(RuntimeError):
    """Raised when we fail to transform the user's query into a known location."""
