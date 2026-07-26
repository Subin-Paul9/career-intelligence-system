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


class InterviewReport(Base):
    __tablename__ = "interview_reports"

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
        unique=True,
    )

    technical_score = Column(
        Float,
        nullable=True,
    )

    communication_score = Column(
        Float,
        nullable=True,
    )

    problem_solving_score = Column(
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

    strengths = Column(
        Text,
        nullable=True,
    )

    weaknesses = Column(
        Text,
        nullable=True,
    )

    missing_topics = Column(
        Text,
        nullable=True,
    )

    learning_resources = Column(
        Text,
        nullable=True,
    )

    suggested_projects = Column(
        Text,
        nullable=True,
    )

    ai_summary = Column(
        Text,
        nullable=True,
    )

    recommendation = Column(
        Text,
        nullable=True,
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
        back_populates="report",
    )

    feedback = relationship(
        "InterviewFeedback",
        back_populates="report",
        uselist=False,
        cascade="all, delete-orphan",
    )