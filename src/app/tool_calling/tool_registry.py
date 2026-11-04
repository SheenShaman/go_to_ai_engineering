from app.tool_calling.tools import get_weather

TOOL_REGISTRY = {
    "get_weather": get_weather,
}
