"""Run: python -m unittest test_weather.py -v   (no internet needed)"""
import unittest
from unittest.mock import patch, Mock

import requests
import weather_api as api

FAKE = {"name": "Trichy", "sys": {"country": "IN"},
        "main": {"temp": 31.4, "feels_like": 35.2, "humidity": 60, "pressure": 1008},
        "wind": {"speed": 3.5}, "weather": [{"description": "clear sky"}]}


def fake_response(code, data=None):
    r = Mock(status_code=code)
    r.json.return_value = data or {}
    r.raise_for_status.side_effect = (
        None if code == 200 else requests.exceptions.HTTPError())
    return r


class WeatherTests(unittest.TestCase):
    @patch("weather_api.requests.get", return_value=fake_response(200, FAKE))
    def test_valid_city(self, _):
        w = api.get_weather("  Trichy ")        # extra spaces also OK
        self.assertEqual(w["city"], "Trichy, IN")
        self.assertEqual(w["temp"], 31)
        self.assertEqual(w["description"], "Clear Sky")

    def test_empty_city(self):
        with self.assertRaises(ValueError):
            api.get_weather("   ")

    @patch("weather_api.requests.get", return_value=fake_response(404))
    def test_invalid_city(self, _):
        with self.assertRaises(LookupError):
            api.get_weather("Xyzabc")

    @patch("weather_api.requests.get", return_value=fake_response(401))
    def test_invalid_key(self, _):
        with self.assertRaises(api.ApiKeyError):
            api.get_weather("Trichy")

    @patch("weather_api.requests.get", side_effect=requests.exceptions.ConnectionError)
    def test_no_internet(self, _):
        with self.assertRaises(requests.exceptions.RequestException):
            api.get_weather("Trichy")


if __name__ == "__main__":
    unittest.main()
