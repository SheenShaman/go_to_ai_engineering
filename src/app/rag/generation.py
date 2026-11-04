from app.constants import MODEL, SYSTEM_PROMPT_DOCS_AGENT
from app.llm_client import client
from app.schemas import Chunk, GenerationAnswer


def get_user_prompt(context: list, question: str) -> str:
    return f"""
    Контекст документации:
    <context>
    {context}
    </context>

    Вопрос пользователя:
    {question}

    Дай ответ на основании контекста и укажи источники.
    """


def get_context(chunks: list[Chunk]) -> list:
    context_parts = []
    for chunk in chunks:
        context_parts.append(
            f"""
            Источник: {chunk.filename}
            Чанк: {chunk.chunk_index}
            Содержимое:
            {chunk.content}
            """
        )
    context = "\n---\n".join(context_parts)
    return context


def generation_answer(
    question: str,
    chunks: list[Chunk],
) -> GenerationAnswer:
    if not chunks:
        return GenerationAnswer(
            answer="В документации не найден подходящий контекст.",
            sources=[],
        )

    context = get_context(chunks)
    user_prompt = get_user_prompt(context, question)
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT_DOCS_AGENT,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    with client:
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT_DOCS_AGENT,
            input=messages,
        )

    answer = response.output_text
    sources = [
        {
            "filename": chunk.filename,
            "chunk_index": chunk.chunk_index,
        }
        for chunk in chunks
    ]

    return GenerationAnswer(
        answer=answer,
        sources=sources,
    )
