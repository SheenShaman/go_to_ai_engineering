from typing import Any


def get_weather(city: str) -> dict[str, Any]:
    """
    Fake weather tool.

    Later this can call a real weather API.
    """

    weather_data = {
        "Амстердам": {
            "температура": 14,
            "состояние": "cloudy",
        },
        "Лондон": {
            "температура": 12,
            "состояние": "rainy",
        },
        "Берлин": {
            "температура": 16,
            "состояние": "sunny",
        },
    }

    return weather_data.get(
        city,
        {
            "температура": None,
            "состояние": None,
        },
    )
