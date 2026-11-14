from fastapi import FastAPI

from app.api import conversations

app = FastAPI()

app.include_router(conversations.router)
