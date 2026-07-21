from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Role of the sender (e.g., user, assistant, system)
    role = Column(
        String(20),
        nullable=False,
    )

    # Message content
    message = Column(
        Text,
        nullable=False,
    )

    # Token usage statistics
    prompt_tokens = Column(
        Integer,
        default=0,
        nullable=False,
    )

    response_tokens = Column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    conversation = relationship(
        "Conversation",
        back_populates="chat_history",
    )

    feedback = relationship(
        "AssistantFeedback",
        back_populates="chat",
        uselist=False,
        cascade="all, delete-orphan",
    )