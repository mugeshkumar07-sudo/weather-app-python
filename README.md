# Weather App using Python

Simple desktop weather app built with Python, Tkinter and the OpenWeatherMap API.
Summer Internship project - Fantasy Solution, Trichy (June 2026).

## Features
- Search current weather by city name
- Shows temperature, feels-like, humidity, wind speed, pressure, sky condition
- Error messages for empty input, unknown city, invalid API key, no internet
- Search history saved in SQLite (`history.db`)

## Setup
1. Install Python 3.10+
2. `pip install -r requirements.txt`
3. Get a free API key from https://openweathermap.org/api
4. Set the key (do NOT put it in the code):
   - Windows (CMD): `set OPENWEATHER_API_KEY=your_key`
   - Windows (PowerShell): `$env:OPENWEATHER_API_KEY="your_key"`
   - Linux/Mac: `export OPENWEATHER_API_KEY=your_key`
5. Run: `python app.py`

## Tests
`python -m unittest test_weather.py -v`

## Author
Mugeshkumar M - B.E. CSE, University College of Engineering (BIT Campus), Anna University, Trichy
