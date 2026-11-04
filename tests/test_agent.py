from src.app.agent import run_agent
from src.app.schemas import MessageHistory


def test_agent(user_message: str):
    try:
        return run_agent(
            MessageHistory(
                message=user_message,
            ),
            stream=True,
        )

    except Exception as error:
        return f"\nОшибка: {error}"


print(test_agent("Какая погода в Амстердаме?"))
print(test_agent("Какая погода в Москве?"))
print(test_agent("Мне нужно передать название города?"))
