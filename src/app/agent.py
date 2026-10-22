import json
from pydantic import ValidationError

from app.config import SYSTEM_PROMPT
from app.tool_definition import TOOLS
from app.tool_registry import TOOL_REGISTRY
from app.llm import client
from app.output_models import AgentResponse

from openai import RateLimitError

# Нужно ли уточнение, если я не указал город?
MODELS = [
    "xingchen-agi/xing4.0-29b-a4b:free",
    "dots-studio/dots-3-note-preview:free",
    "recursive/flint-v1.0:free",
]

RESPONSE_FORMAT = {
    "type": "json_schema",
    "name": "agent_response",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
            },
            "needs_follow_up": {
                "type": "boolean",
            },
        },
        "required": ["answer", "needs_follow_up"],
        "additionalProperties": False,
    },
}


def run_agent(
    user_message: str,
    history: list | None = None,
    *,
    stream: bool = True,
    structured: bool = False,
) -> str | AgentResponse:
    if history is None:
        history = []

    input_items = [
        *history,
        {
            "role": "user",
            "content": user_message,
        },
    ]

    for model in MODELS:
        try:
            while True:
                request = {
                    "model": model,
                    "instructions": SYSTEM_PROMPT,
                    "input": input_items,
                    "tools": TOOLS,
                    "tool_choice": "required",
                    # "extra_body": {
                    #     "provider": {
                    #         "require_parameters": True,
                    #     },
                    # },
                }
                if structured:
                    request["text"] = {
                        "format": RESPONSE_FORMAT,
                    }

                if stream and not structured:
                    response_stream = client.responses.create(
                        **request,
                        stream=True,
                    )

                    response = None

                    for event in response_stream:
                        if event.type == "response.output_text.delta":
                            print(event.delta, end="", flush=True)
                        elif event.type == "response.completed":
                            response = event.response

                    if response is None:
                        raise RuntimeError("Stream ended without a completed response")

                else:
                    response = client.responses.create(**request)

                input_items.extend(response.output)

                tool_calls = [
                    item for item in response.output if item.type == "function_call"
                ]
                for item in response.output:
                    print("Model", model)
                    print("TYPE:", item.type)
                    print("ITEM:", item)

                if not tool_calls:
                    answer = response.output_text
                    print(repr(answer))

                    if structured:
                        try:
                            result = AgentResponse.model_validate_json(answer)
                            history[:] = input_items
                            return result
                        except ValidationError as e:
                            print(f"Некорректный structured output: {e}")
                            print(f"Ответ модели: {answer!r}")
                            raise

                    history[:] = input_items
                    return answer

                for tool_call in tool_calls:
                    tool = TOOL_REGISTRY.get(tool_call.name)

                    if tool is None:
                        raise ValueError(f"Unknow tool: {tool_call.name}")

                    arguments = json.loads(tool_call.arguments)
                    result = tool(**arguments)

                    input_items.append(
                        {
                            "type": "function_call_output",
                            "call_id": tool_call.call_id,
                            "output": json.dumps(
                                result, ensure_ascii=False, default=str
                            ),
                        }
                    )

        except RateLimitError:
            continue

    raise RuntimeError("All configured models failed with rate limits.")
