from pydantic import BaseModel, Field


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


class MessageHistory(BaseModel):
    message: str
    history: list[dict[str, str]] = Field(default_factory=list)


class AgentResponse(BaseModel):
    answer: str = Field(description="Ответ пользователю")
    needs_follow_up: bool = Field(
        description="Нужно ли задать пользователю уточняющий вопрос"
    )
