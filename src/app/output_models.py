from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    answer: str = Field(description="Ответ пользователю")
    needs_follow_up: bool = Field(
        description="Нужно ли задать пользователю уточняющий вопрос"
    )
