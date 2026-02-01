"""
Tools package for Michael's Retirement Travel Planner.

This package contains tools for:
- Geocoding city names to coordinates
- Getting weather forecasts
- Checking air quality
- Finding tourist attractions
"""

from .geocode import geocode_city
from .weather import get_weather, get_clothing_recommendation
from .air_quality import get_air_quality, get_health_recommendation
from .places import get_places, format_places_for_display

__all__ = [
    'geocode_city',
    'get_weather',
    'get_clothing_recommendation',
    'get_air_quality',
    'get_health_recommendation',
    'get_places',
    'format_places_for_display'
]