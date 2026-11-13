from pydantic import BaseModel, Field
from datetime import datetime


class Chunk(BaseModel):
    chunk_id: int
    filename: str
    chunk_index: int
    content: str
    distance: float


class GenerationAnswer(BaseModel):
    answer: str
    sources: list[dict[str, str | int]]


class ChunksConfig(BaseModel):
    data: str
    chunk_size: int = 750
    overlap: int = 100


class AgentResponse(BaseModel):
    answer: str = Field(description="Ответ пользователю")
    needs_follow_up: bool = Field(
        description="Нужно ли задать пользователю уточняющий вопрос"
    )


class Conversation(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class Message(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: dict
    created_at: datetime = Field(default=datetime.now())


class UsersQuery(BaseModel):
    users_message: str
    users_history: list[dict] = Field(default_factory=list)
