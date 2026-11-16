"""
Conversation service
"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.conversations import ConversationsRepo
from src.app.schemas.conversations import (
    CreateConversation,
    ReadConversation,
    UpdateConversation,
)


class ConversationService:
    """Service for Conversation business logic."""

    @staticmethod
    async def get_all(session: AsyncSession) -> list[ReadConversation]:
        """Get all conversations."""
        conversations = await ConversationsRepo.get_all(session=session)
        return conversations

    @staticmethod
    async def get_by_id(
        session: AsyncSession, conversation_id: int
    ) -> ReadConversation | None:
        """Get a conversation by its ID."""
        conversation = await ConversationsRepo.get_one_by_id(
            session=session, id_=conversation_id
        )
        if not conversation:
            return None
        return conversation

    @staticmethod
    async def create(
        session: AsyncSession, conversation_data: CreateConversation
    ) -> ReadConversation:
        """Create a new conversation."""
        conversation = await ConversationsRepo.create(
            session=session,
            user_id=conversation_data.user_id,
            title=conversation_data.title,
        )
        return conversation

    @staticmethod
    async def update(
        session: AsyncSession,
        conversation_id: int,
        conversation_data: UpdateConversation,
    ) -> ReadConversation | None:
        """Update a conversation by its ID."""
        conversation = await ConversationsRepo.update_by_id(
            session,
            id_=conversation_id,
            title=conversation_data.title,
        )
        if not conversation:
            return None
        return conversation

    @staticmethod
    async def delete(session: AsyncSession, conversation_id: int) -> bool:
        """Delete a conversation by its ID."""
        await ConversationsRepo.delete_by_id(
            session=session, id_=conversation_id
        )
