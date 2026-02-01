# Michael’s Retirement Travel Planner

A LangChain-powered AI agent that assists with retirement travel planning by
analyzing real-time **weather**, **air quality**, and **nearby attractions**
for multiple cities using real-world APIs.

This project was developed as part of **Agentic AI Project 1** and follows all
course requirements for LangChain v1.2+, tool usage, and secure API handling.

---

## Features

- City geocoding using Google Maps
- Weather forecasts with clothing recommendations
- Air quality analysis with health guidance
- Tourist attraction discovery (parks, museums, landmarks)
- Interactive follow-up questions for deeper city insights
- Travel reports automatically saved in **TXT** and **JSON** formats
- AI agent orchestration using **LangChain v1.2+**

---

## Tech Stack

- Python 3.10+
- LangChain v1.2+
- uv (package and environment management)
- Google Maps APIs
- Open-Meteo Weather API
- OpenAI (via `langchain-openai`)

---

## APIs Used

- **Google Maps Geocoding API** – convert city names to coordinates  
- **Google Places API** – find nearby attractions  
- **Google Air Quality API** – retrieve AQI and health recommendations  
- **Open-Meteo API** – weather forecasts (no API key required)

---

## Weather Data Source (Required Explanation)

Weather forecasts are retrieved using the **Open-Meteo API**, a free and reliable
public weather service. This approach avoids unnecessary Google billing while
still providing accurate short-term forecasts suitable for travel planning.

---

## Project Structure

AgenticAI_Project1/
│
├── main.py
├── pyproject.toml
├── README.md
├── uv.lock
├── tools/
│ ├── geocode.py
│ ├── weather.py
│ ├── air_quality.py
│ └── places.py


---

## Setup & Installation

### Install dependencies (using uv)

```bash
uv sync

---

## Environment variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here



## How to Run 

uv run main.py

You will be prompted to enter a natural-language travel request, for example:
Plan a retirement trip to Toronto and Chicago.


## Output Files

For detailed runs, the application automatically saves results to:
- A human-readable TXT travel report
- A structured JSON file for further analysis
- Both files are timestamped and stored in the project root.

## How It Works

- The agent is created using LangChain’s create_agent
- External capabilities are registered using Tool.from_function
- The agent dynamically decides which tools to call based on user input
- Inputs are accepted as natural language
- API keys are securely loaded from environment variables
- All external data retrieval is handled using the requests library

## Course Compliance Notes
- Uses LangChain v1.2+
- Uses create_agent (no custom agent classes)
- Uses LangChain’s built-in tool abstractions
- Uses requests for all external API calls
- Uses pyproject.toml with uv (no requirements.txt)
- Secure secret handling via environment variables
- Designed to work across multiple test cases (robust, non-toy project)

## Acknowledgments
- Developed as part of the Foundation of Professional Analytics program,
- Saint Mary’s University.
