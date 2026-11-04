TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": (
            "Get the current weather for a city. "
            "Use this tool when the user asks about weather."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, for example Амстердам",
                }
            },
            "required": ["city"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]
