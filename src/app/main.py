from fastapi import FastAPI

from src.app.api import conversations

app = FastAPI()

app.include_router(conversations.router)
