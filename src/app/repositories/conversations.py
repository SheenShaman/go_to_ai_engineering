from src.app.database.models import Conversation
from src.app.repositories.base import BaseRepo


class ConversationsRepo(BaseRepo):
    model = Conversation
