"""
Настройки LLM
"""

from openai import OpenAI

from app.config import OPEN_ROUTER_KEY

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPEN_ROUTER_KEY,
)

def ask_llm(prompt: str) -> str:
    response = client.responses.create(
        model="qwen/qwen3.8-27b:free",
        input=prompt,
        temperature=0.3,
    )
    return response.output_text
