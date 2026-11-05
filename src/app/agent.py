import json
from openai import RateLimitError

from app.constants import MAX_TOOL_ROUNDS, MODEL, SYSTEM_PROMPT_WITH_TOOLS_AGENT
from app.llm_client import client
from app.logging import logger
from app.schemas import MessageHistory
from app.tool_calling.tool_schemas import TOOLS
from app.tool_calling.tool_registry import TOOL_REGISTRY


def run_agent(
    user_query: MessageHistory,
    stream: bool = True,
) -> str:

    input_items = [
        *user_query.history,
        {"role": "user", "content": user_query.message},
    ]
    tool_rounds = 0

    # Этап 1. Вызываем модель и обрабатываем инструменты.
    while True:
        try:
            if stream:
                response_stream = client.responses.create(
                    model=MODEL,
                    instructions=SYSTEM_PROMPT_WITH_TOOLS_AGENT,
                    input=input_items,
                    tools=TOOLS,
                    tool_choice="auto",
                    temperature=0.1,
                    stream=True,
                )

                completed_response = None

                for event in response_stream:
                    if event.type == "response.completed":
                        completed_response = event.response

                    elif event.type in ("response.failed", "error"):
                        raise RuntimeError(f"Agent error: {event}")

                if completed_response is None:
                    raise RuntimeError("Модель не вернула завершенный ответ.")

                response = completed_response

            else:
                response = client.responses.create(
                    model=MODEL,
                    instructions=SYSTEM_PROMPT_WITH_TOOLS_AGENT,
                    input=input_items,
                    tools=TOOLS,
                    tool_choice="auto",
                    temperature=0.1,
                )
        except RateLimitError:
            logger.exception("[Agent] Rate limit exceeded")
            raise RateLimitError

        # Сценарий 1. Модель запросила инструменты.
        tool_calls = [item for item in response.output if item.type == "function_call"]

        if tool_calls:
            if tool_rounds >= MAX_TOOL_ROUNDS:
                logger.warning("[Agent] Maximum tool rounds exceeded")

                return (
                    "Не удалось завершить задачу: превышен лимит вызовов инструментов."
                )

            # Сохраняем ответ модели с вызовами инструментов.
            input_items.extend(response.output)

            for tool_call in tool_calls:
                logger.info(f"[Tool] {tool_call.name}")
                tool = TOOL_REGISTRY.get(tool_call.name)

                if tool is None:
                    result = {
                        "error": f"Unknown tool: {tool_call.name}",
                    }

                else:
                    try:
                        arguments = json.loads(tool_call.arguments)
                        if not isinstance(arguments, dict):
                            raise ValueError("Tool arguments must be a Json object")
                        result = tool(**arguments)

                    except Exception as exception:
                        logger.exception(f"[Tool error] {tool_call.name}")
                        result = {"error": str(exception)}

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
            tool_rounds += 1
            continue

        # Сценарий 2. Модель вернула обычный текст.
        answer = response.output_text or ""
        logger.info(f"[Answer] {answer}")

        input_items.extend(response.output)
        user_query.history[:] = input_items

        return answer
