from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class InterviewFeedback(Base):
    __tablename__ = "interview_feedback"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    report_id = Column(
        Integer,
        ForeignKey(
            "interview_reports.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    strengths = Column(
        Text,
        nullable=True,
    )

    weaknesses = Column(
        Text,
        nullable=True,
    )

    missing_skills = Column(
        Text,
        nullable=True,
    )

    improvement_suggestions = Column(
        Text,
        nullable=True,
    )

    learning_resources = Column(
        Text,
        nullable=True,
    )

    mentor_advice = Column(
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

    report = relationship(
        "InterviewReport",
        back_populates="feedback",
    )