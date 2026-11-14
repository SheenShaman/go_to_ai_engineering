from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: dict
    created_at: datetime
