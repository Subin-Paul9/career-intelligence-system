from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    session_id = Column(
        Integer,
        ForeignKey(
            "interview_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    question = Column(
        Text,
        nullable=False,
    )

    category = Column(
        String(50),
        nullable=False,
    )

    difficulty = Column(
        String(20),
        nullable=False,
    )

    question_order = Column(
        Integer,
        nullable=False,
    )

    expected_answer = Column(
        Text,
        nullable=True,
    )

    generated_by_ai = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # -------------------------
    # Relationships
    # -------------------------

    session = relationship(
        "InterviewSession",
        back_populates="questions",
    )

    answer = relationship(
        "InterviewAnswer",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan",
    )