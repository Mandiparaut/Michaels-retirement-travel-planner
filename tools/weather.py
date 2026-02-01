import requests

URL = "https://api.open-meteo.com/v1/forecast"

def get_weather(lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,is_day",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 3
    }

    response = requests.get(URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    weather_codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 51: "Light drizzle", 61: "Slight rain",
        63: "Moderate rain", 65: "Heavy rain", 71: "Snow"
    }

    current = data["current"]
    daily = data["daily"]

    return {
        "temperature_c": round(current["temperature_2m"], 1),
        "condition": weather_codes.get(current["weather_code"], "Unknown"),
        "wind_speed_kmh": round(current["wind_speed_10m"], 1),
        "needs_umbrella": current["precipitation"] > 0
    }


def get_clothing_recommendation(weather: dict) -> str:
    temp = weather["temperature_c"]

    if temp < 10:
        return "Warm jacket and long pants"
    elif temp < 20:
        return "Light jacket recommended"
    else:
        return "Light clothing"
