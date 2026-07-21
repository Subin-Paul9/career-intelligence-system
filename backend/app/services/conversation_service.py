from sqlalchemy.orm import Session

from app.models.chat_history import ChatHistory
from app.models.conversation import Conversation


class ConversationService:
    """
    Service responsible for managing user conversations.
    """

    def __init__(self, db: Session):
        self.db = db

    def start_conversation(
        self,
        user_id: int,
        title: str,
    ) -> Conversation:
        """
        Create and save a new conversation.
        """

        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def rename_conversation(
        self,
        conversation_id: int,
        title: str,
    ) -> Conversation | None:
        """
        Rename an existing conversation.
        """

        conversation = (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if not conversation:
            return None

        conversation.title = title

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_user_conversations(
        self,
        user_id: int,
    ) -> list[Conversation]:
        """
        Retrieve all conversations belonging to a user,
        ordered by the most recently updated.
        """

        return (
            self.db.query(Conversation)
            .filter(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.updated_at.desc()
            )
            .all()
        )

    def get_conversation_history(
        self,
        conversation_id: int,
    ) -> list[ChatHistory]:
        """
        Retrieve all chat messages for a conversation
        in chronological order.
        """

        return (
            self.db.query(ChatHistory)
            .filter(
                ChatHistory.conversation_id == conversation_id
            )
            .order_by(
                ChatHistory.created_at.asc()
            )
            .all()
        )

    def delete_chat_history(
        self,
        conversation_id: int,
    ) -> bool:
        """
        Delete all chat messages for a conversation while
        keeping the conversation itself.
        """

        deleted_rows = (
            self.db.query(ChatHistory)
            .filter(
                ChatHistory.conversation_id == conversation_id
            )
            .delete(
                synchronize_session=False
            )
        )

        self.db.commit()

        return deleted_rows > 0

    def delete_conversation(
        self,
        conversation_id: int,
    ) -> bool:
        """
        Delete a conversation and all associated chat history.
        """

        conversation = (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

        if not conversation:
            return False

        self.db.delete(conversation)
        self.db.commit()

        return True