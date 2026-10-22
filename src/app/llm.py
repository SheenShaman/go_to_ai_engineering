"""
Настройки LLM
"""

from openai import OpenAI

from app.config import OPEN_ROUTER_KEY

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPEN_ROUTER_KEY,
)
