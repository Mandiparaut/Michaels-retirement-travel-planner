import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
URL = "https://places.googleapis.com/v1/places:searchNearby"

HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating"
}

def get_places(lat: float, lon: float, place_types: list[str], radius: int = 5000) -> dict:
    results = {}

    for p_type in place_types:
        payload = {
            "includedTypes": [p_type],
            "maxResultCount": 5,
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": lat, "longitude": lon},
                    "radius": radius
                }
            }
        }

        response = requests.post(URL, headers=HEADERS, json=payload, timeout=10)
        response.raise_for_status()

        places = response.json().get("places", [])
        results[p_type] = [
            {
                "name": p.get("displayName", {}).get("text", "Unknown"),
                "address": p.get("formattedAddress", "N/A"),
                "rating": p.get("rating", "No rating")
            }
            for p in places
        ]

    return results


def format_places_for_display(data: dict) -> str:
    out = []
    for t, places in data.items():
        out.append(f"\n{t.upper()}")
        for p in places:
            out.append(f"- {p['name']} ({p['address']})")
    return "\n".join(out)
