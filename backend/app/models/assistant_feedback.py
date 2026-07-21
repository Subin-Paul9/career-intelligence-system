from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class AssistantFeedback(Base):
    __tablename__ = "assistant_feedback"

    id = Column(Integer, primary_key=True, index=True)

    chat_id = Column(
        Integer,
        ForeignKey("chat_history.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    rating = Column(Integer, nullable=False)

    comment = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    chat = relationship(
        "ChatHistory",
        back_populates="feedback",
    )