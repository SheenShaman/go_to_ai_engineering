from typing import Any


def get_weather(city: str) -> dict[str, Any]:
    """
    Fake weather tool.

    Later this can call a real weather API.
    """

    weather_data = {
        "Amsterdam": {
            "temperature": 14,
            "condition": "cloudy",
        },
        "London": {
            "temperature": 12,
            "condition": "rainy",
        },
        "Berlin": {
            "temperature": 16,
            "condition": "sunny",
        },
    }

    return weather_data.get(
        city,
        {
            "temperature": None,
            "condition": None,
        },
    )
