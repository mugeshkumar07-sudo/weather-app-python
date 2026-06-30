"""Weather logic: calls OpenWeatherMap, validates input, stores history in SQLite."""
import os
import sqlite3
from datetime import datetime

import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DB_FILE = "history.db"


class ApiKeyError(Exception):
    """Raised when the API key is wrong (HTTP 401)."""


def get_weather(city):
    city = city.strip()
    if not city:
        raise ValueError("Please enter a city name")

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params, timeout=10)

    if response.status_code == 404:
        raise LookupError("City not found. Please check the spelling and try again.")
    if response.status_code == 401:
        raise ApiKeyError("Invalid API key. Check OPENWEATHER_API_KEY.")
    response.raise_for_status()

    data = response.json()
    return {
        "city": f"{data['name']}, {data['sys']['country']}",
        "temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"].title(),
    }


def init_db():
    with sqlite3.connect(DB_FILE) as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS history (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   city TEXT, temperature REAL,
                   condition TEXT, searched_at TEXT)"""
        )


def save_history(w):
    with sqlite3.connect(DB_FILE) as con:
        con.execute(
            "INSERT INTO history (city, temperature, condition, searched_at) VALUES (?,?,?,?)",
            (w["city"], w["temp"], w["description"],
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )


def get_history(limit=5):
    with sqlite3.connect(DB_FILE) as con:
        return con.execute(
            "SELECT city, temperature, condition, searched_at "
            "FROM history ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
