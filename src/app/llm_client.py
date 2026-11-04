"""
Настройки LLM
"""

from openai import OpenAI

from app.constants import OPEN_ROUTER_URL, OPEN_ROUTER_KEY

client = OpenAI(
    base_url=OPEN_ROUTER_URL,
    api_key=OPEN_ROUTER_KEY,
)
