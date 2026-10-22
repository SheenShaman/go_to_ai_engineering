"""
Настройки подключения
"""

import os

from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
MODEL = os.getenv("MODEL")

SYSTEM_PROMPT = """
Ты — полезный ИИ-агент.
Отвечай на русском языке.
Используй инструменты, если они нужны для выполнения задачи.
Не выдумывай результаты работы инструментов.
Если информации недостаточно, сообщи об этом.
"""

if not OPEN_ROUTER_KEY:
    raise RuntimeError("OPEN_ROUTER_KEY not set")
