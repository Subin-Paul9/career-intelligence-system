from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    question_id = Column(
        Integer,
        ForeignKey(
            "interview_questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    answer = Column(
        Text,
        nullable=False,
    )

    ai_feedback = Column(
        Text,
        nullable=True,
    )

    technical_score = Column(
        Float,
        nullable=True,
    )

    communication_score = Column(
        Float,
        nullable=True,
    )

    confidence_score = Column(
        Float,
        nullable=True,
    )

    overall_score = Column(
        Float,
        nullable=True,
    )

    response_time = Column(
        Integer,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # -------------------------
    # Relationships
    # -------------------------

    question = relationship(
        "InterviewQuestion",
        back_populates="answer",
    )