"""
Настройки подключения
"""

import os

from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")

if not OPEN_ROUTER_KEY:
    raise RuntimeError("OPEN_ROUTER_KEY not set")