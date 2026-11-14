from app.database.models import Conversation
from app.repositories.base import BaseRepo


class ConversationsRepo(BaseRepo):
    model = Conversation
