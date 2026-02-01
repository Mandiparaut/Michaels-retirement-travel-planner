import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
URL = "https://airquality.googleapis.com/v1/currentConditions:lookup"

def get_air_quality(lat: float, lon: float) -> dict:
    payload = {
        "location": {
            "latitude": lat,
            "longitude": lon
        }
    }

    response = requests.post(
        URL,
        json=payload,
        params={"key": API_KEY},
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    index = data.get("indexes", [{}])[0]
    aqi = index.get("aqi", "N/A")

    return {
        "aqi": aqi,
        "category": index.get("category", "Unknown"),
        "health_recommendation": get_health_recommendation(aqi)
    }


def get_health_recommendation(aqi):
    if not isinstance(aqi, int):
        return "Air quality data unavailable"
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    else:
        return "Unhealthy - limit outdoor activity"
