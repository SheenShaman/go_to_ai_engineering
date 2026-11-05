from typing import Any


def get_weather(city: str) -> dict[str, Any]:
    """
    Fake weather tool.

    Later this can call a real weather API.
    """

    weather_data = {
        "амстердам": {
            "температура": 14,
            "состояние": "cloudy",
        },
        "лондон": {
            "температура": 12,
            "состояние": "rainy",
        },
        "берлин": {
            "температура": 16,
            "состояние": "sunny",
        },
    }

    return weather_data.get(
        city.strip().lower(),
        {
            "температура": None,
            "состояние": None,
            "ошибка": f"Нет данных для города: {city}",
        },
    )
