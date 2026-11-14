from datetime import datetime

from pydantic import BaseModel


class ReadConversation(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class CreateConversation(BaseModel):
    user_id: int
    title: str


class UpdateConversation(BaseModel):
    title: str
