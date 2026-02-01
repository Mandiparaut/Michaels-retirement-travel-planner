"""
Michael's Retirement Travel Planner
Course-compliant LangChain Agent (v1.2+)
"""

import json
from datetime import datetime
import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from tools.geocode import geocode_city
from tools.weather import get_weather, get_clothing_recommendation
from tools.air_quality import get_air_quality
from tools.places import get_places, format_places_for_display

# ---------------------------------------------------------------------
# ENV
# ---------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------
# TOOLS
# ---------------------------------------------------------------------
tools = [
    Tool.from_function(geocode_city, "geocode_city", "Convert city to coordinates"),
    Tool.from_function(get_weather, "get_weather", "Get weather for coordinates"),
    Tool.from_function(get_air_quality, "get_air_quality", "Get air quality for coordinates"),
    Tool.from_function(get_places, "get_places", "Find nearby attractions"),
]

# ---------------------------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------------------------
def save_output(text_output: str, json_output: dict):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    txt_file = f"travel_report_{timestamp}.txt"
    json_file = f"travel_report_{timestamp}.json"

    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(text_output)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=2)

    print(f"\n✅ Output saved to:")
    print(f" - {txt_file}")
    print(f" - {json_file}")

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
def main():
    output_log = []   # <- capture everything printed
    json_results = {}

    def log(text):
        print(text)
        output_log.append(text)

    log("=" * 60)
    log("MICHAEL'S RETIREMENT TRAVEL PLANNER")
    log("=" * 60)

    if not os.getenv("OPENAI_API_KEY"):
        log("ERROR: OPENAI_API_KEY not set")
        return

    if not os.getenv("GOOGLE_MAPS_API_KEY"):
        log("ERROR: GOOGLE_MAPS_API_KEY not set")
        return

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_agent(model, tools)

    log("\nEnter your travel request below.")
    log("Example: Plan a retirement trip to Toronto and Chicago.\n")

    user_prompt = input("Your request: ")

    log("\nPlanning trip...\n")

    result = agent.invoke({"messages": [("user", user_prompt)]})

    log("\n=== MICHAEL'S RETIREMENT TRAVEL REPORT ===\n")

    if isinstance(result, dict) and "messages" in result:
        for msg in reversed(result["messages"]):
            if msg.type == "ai":
                log(msg.content)
                break

    follow_up = input(
        "\nWould you like more specific information "
        "(weather, air quality, attractions)? (yes/no): "
    ).strip().lower()

    if follow_up != "yes":
        save_output("\n".join(output_log), {})
        log("\nThank you for using Michael’s Retirement Travel Planner!")
        return

    log("\nGenerating detailed information...\n")

    cities_input = input(
        "Enter the cities again (comma separated, e.g. New York, Miami): "
    )

    cities = [c.strip() for c in cities_input.split(",") if c.strip()]

    for city in cities:
        log("\n" + "=" * 60)
        log(city.upper())
        log("=" * 60)

        try:
            lat, lon, formatted = geocode_city(city)
            log(f"\nLocation: {formatted}")
            log(f"Coordinates: {lat}, {lon}")

            weather = get_weather(lat, lon)
            air = get_air_quality(lat, lon)
            places = get_places(lat, lon, ["tourist_attraction", "museum", "park"])

            log("\nWeather:")
            log(f"Temperature: {weather['temperature_c']} °C")
            log(f"Condition: {weather['condition']}")
            log(f"Wind: {weather['wind_speed_kmh']} km/h")
            log(f"Clothing: {get_clothing_recommendation(weather)}")

            log("\nAir Quality:")
            log(f"AQI: {air['aqi']}")
            log(f"Category: {air['category']}")
            log(f"Health Advice: {air['health_recommendation']}")

            log("\nNearby Attractions:")
            log(format_places_for_display(places))

            json_results[city] = {
                "location": formatted,
                "coordinates": {"lat": lat, "lon": lon},
                "weather": weather,
                "air_quality": air,
                "places": places,
            }

        except Exception as e:
            log(f"Error processing {city}: {e}")

    save_output("\n".join(output_log), json_results)
    log("\nThank you for using Michael’s Retirement Travel Planner!")

# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()
