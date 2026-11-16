"""
Api Conversations

get_conversations -> list[Conversation] 200
get_conversation_by_id -> Conversation 200
create_conversation -> Conversation 201
update_conversation -> Conversation 200
delete_conversation -> No content 204
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database.session import get_db_session
from src.app.schemas.conversations import CreateConversation, ReadConversation
from src.app.services.conversations import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get(
    "", response_model=list[ReadConversation], status_code=status.HTTP_200_OK
)
async def get_conversations(session: AsyncSession = Depends(get_db_session)):
    return await ConversationService.get_all(session)


@router.get(
    "/{conversation_id}",
    response_model=ReadConversation,
    status_code=status.HTTP_200_OK,
)
async def get_conversation_by_id(
    conversation_id: int, session: AsyncSession = Depends(get_db_session)
):
    conversation = await ConversationService.get_by_id(
        session,
        conversation_id,
    )
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return conversation


@router.post(
    "", response_model=ReadConversation, status_code=status.HTTP_201_CREATED
)
async def create_conversation(
    conversation: CreateConversation,
    session: AsyncSession = Depends(get_db_session),
):
    return await ConversationService.create(session, conversation)


@router.patch(
    "/{conversation_id}",
    response_model=ReadConversation,
    status_code=status.HTTP_200_OK,
)
async def update_conversation_by_id(
    conversation_id: int,
    updated_conversation: ReadConversation,
    session: AsyncSession = Depends(get_db_session),
):
    conversation = await ConversationService.update(
        session,
        conversation_id,
        updated_conversation.model_dump(exclude_unset=True),
    )
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_by_id(
    conversation_id: int, session: AsyncSession = Depends(get_db_session)
):
    await ConversationService.delete(session, conversation_id)
