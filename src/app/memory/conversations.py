import psycopg

import json
from app.constants import DATABASE_URL
from app.logging import logger
from app.schemas import Conversation, Message


# Conversations
def get_conversation_by_user_id(user_id: int) -> Conversation:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, user_id, title, created_at, updated_at
                FROM conversations
                WHERE user_id = %s
                """,
                (user_id,),
            )
            row = cur.fetchone()

    return Conversation(
        id=row[0],
        user_id=row[1],
        title=row[2],
        created_at=row[3],
        updated_at=row[4],
    )


def create_conversation(
        conversation: Conversation
) -> int:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO conversations (id, user_id, title)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                RETURNING id
                """,
                (conversation.id, conversation.user_id, conversation.title),
            )
            row = cur.fetchone()

            if row is None:
                cur.execute(
                    """
                    SELECT id 
                    FROM conversations 
                    WHERE id = %s
                    """,
                    (conversation.id,),
                )
                conversation_id = cur.fetchone()[0]
                return conversation_id

            conversation_id = row[0]

    return conversation_id


# Messages
def get_messages_by_conversation_id(conversation_id: int) -> list[Message]:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, conversation_id, role, content, created_at
                FROM messages
                WHERE conversation_id = %s
                ORDER BY created_at DESC
                """,
                (conversation_id,),
            )
            rows = cur.fetchall()

    return [
        Message(
            id=row[0],
            conversation_id=row[1],
            role=row[2],
            content=row[3],
            created_at=row[4],
        )
        for row in rows
    ]


def create_message(
        conversation: Conversation,
        message: Message,
) -> int:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM conversations 
                WHERE id = %s
                """,
                (message.conversation_id,),
            )
            row = cur.fetchone()
            if row is None:
                logger.info("Conversation not found")
                message.conversation_id = create_conversation(conversation)

            content_to_json = json.dumps(message.content, ensure_ascii=False,
                                         indent=4)
            cur.execute(
                """
                INSERT INTO messages (id, conversation_id, role, content)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (message.id, message.conversation_id, message.role,
                 content_to_json)
            )
            row = cur.fetchone()

            message_id = row[0]

    return message_id
