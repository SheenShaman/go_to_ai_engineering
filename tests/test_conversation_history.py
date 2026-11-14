from src.app.memory import conversations


def test_get_conversation():
    conversation = conversations.get_conversation_by_user_id(1)
    assert conversation.id == 1
    assert conversation.user_id == 1
    assert conversation.title == "Test"


def test_get_messages():
    messages = conversations.get_messages_by_conversation_id(1)
    assert len(messages) == 1
    assert messages[0].id == 1
    assert messages[0].conversation_id == 1
    assert messages[0].content == {"message": "Test"}
