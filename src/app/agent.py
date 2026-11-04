import json

from openai import RateLimitError

from app.constants import SYSTEM_PROMPT_WITH_TOOLS_AGENT, MODEL, MAX_TOOL_ROUNDS
from app.llm_client import client
from app.tool_calling.tool_definition import TOOLS
from app.tool_calling.tool_registry import TOOL_REGISTRY
from app.logging import logger
from app.schemas import MessageHistory


def run_agent(
    user_query: MessageHistory,
    stream: bool = True,
) -> str:

    input_items = [
        *user_query.history,
        {"role": "user", "content": user_query.message},
    ]

    # Этап 1. Вызываем модель и обрабатываем инструменты.
    for round_number in range(MAX_TOOL_ROUNDS):
        try:
            response = client.responses.create(
                model=MODEL,
                instructions=SYSTEM_PROMPT_WITH_TOOLS_AGENT,
                input=input_items,
                tools=TOOLS,
                tool_choice="auto",
            )
        except RateLimitError:
            raise

        tool_calls = [item for item in response.output if item.type == "function_call"]

        # Модель не запросила инструменты — переходим
        # к генерации финального ответа.
        if not tool_calls:
            break

        # Сохраняем вызовы модели перед передачей результатов.
        input_items.extend(response.output)

        for tool_call in tool_calls:
            logger.info(f"[Tool] {tool_call.name}")

            tool = TOOL_REGISTRY.get(tool_call.name)

            if tool is None:
                result = {"error": f"Unknown tool: {tool_call.name}"}
            else:
                try:
                    arguments = json.loads(tool_call.arguments)
                    result = tool(**arguments)
                except Exception as exc:
                    result = {"error": str(exc)}
            logger.info(f"[Tool result] {result}")

            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str,
                    ),
                }
            )

    # Этап 2. Генерируем финальный ответ.
    # На этом этапе новые вызовы инструментов запрещены.
    try:
        final_stream = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT_WITH_TOOLS_AGENT,
            input=input_items,
            tools=TOOLS,
            tool_choice="none",
            stream=stream,
        )
    except RateLimitError:
        raise

    if not stream:
        answer = final_stream.output_text
        logger.info(f"[Answer] {answer}")
        user_query.history[:] = input_items + [{"role": "assistant", "content": answer}]
        return answer

    chunks = []
    completed_response = None

    for event in final_stream:
        if event.type == "response.output_text.delta":
            chunks.append(event.delta)
            # logger.info(f"[Stream] {event.delta}")

        elif event.type == "response.completed":
            completed_response = event.response

        elif event.type in ("response.failed", "error"):
            raise RuntimeError(f"Streaming error: {event}")

    answer = "".join(chunks)

    if completed_response is not None:
        input_items.extend(completed_response.output)

    user_query.history[:] = input_items + (
        []
        if completed_response is not None
        else [{"role": "assistant", "content": answer}]
    )

    return answer
