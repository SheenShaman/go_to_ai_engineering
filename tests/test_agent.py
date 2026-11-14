from src.app.agent import run_agent
from src.app.memory.conversations import get_messages_by_conversation_id
from src.app.schemas import UsersQuery


def test_run_agent_simple_query():
    simple_query = "Какая погода в Амстердаме?"
    history = get_messages_by_conversation_id(conversation_id=1)

    answer = run_agent(
        UsersQuery(
            users_message=simple_query,
            users_history=[
                {"role": "user", "content": str(message.content)}
                for message in history
            ],
        ),
        stream=True,
    )

    assert (
        answer.strip()
        == "В Амстердаме облачно, температура воздуха составляет 14°C."
    )


# def test_run_agent_another_city():
#     Придумать предсказуемый формат ответа для тестирования или другой формат
#     тестирования
#     "Какая погода?"
#     simple_query = "Какая погода в Москве?"
#     history = get_messages_by_conversation_id(conversation_id=1)
#
#     answer = run_agent(
#         UsersQuery(
#             users_message=simple_query,
#             users_history=[
#                 {
#                 "role": "user",
#                 "content": str(message.content)
#             }
#             for message in history]
#         ),
#         stream=True,
#     )
#
#     assert "не удалось получить данные о погоде в Москве" in answer.strip()
