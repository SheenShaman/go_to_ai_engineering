"""
Настройки LLM
"""

from openai import OpenAI

from app.constants import OPEN_ROUTER_KEY, OPEN_ROUTER_URL

client = OpenAI(
    base_url=OPEN_ROUTER_URL,
    api_key=OPEN_ROUTER_KEY,
)
