import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
URL = "https://maps.googleapis.com/maps/api/geocode/json"

def geocode_city(city: str):
    response = requests.get(
        URL,
        params={"address": city, "key": API_KEY},
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    if not data["results"]:
        raise ValueError(f"City not found: {city}")

    loc = data["results"][0]["geometry"]["location"]
    name = data["results"][0]["formatted_address"]

    return loc["lat"], loc["lng"], name

