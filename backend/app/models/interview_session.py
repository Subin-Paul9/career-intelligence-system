from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    career_recommendation_id = Column(
        Integer,
        ForeignKey(
            "career_recommendations.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    # =====================================================
    # Retry Interview
    # =====================================================

    retry_of_session_id = Column(
        Integer,
        ForeignKey(
            "interview_sessions.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    attempt_number = Column(
        Integer,
        default=1,
        nullable=False,
    )

    interview_type = Column(
        String(50),
        nullable=False,
    )

    difficulty = Column(
        String(20),
        nullable=False,
    )

    status = Column(
        String(20),
        default="ACTIVE",
        nullable=False,
    )

    total_questions = Column(
        Integer,
        default=10,
        nullable=False,
    )

    answered_questions = Column(
        Integer,
        default=0,
        nullable=False,
    )

    overall_score = Column(
        Float,
        nullable=True,
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    duration = Column(
        Integer,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # =====================================================
    # Relationships
    # =====================================================

    user = relationship(
        "User",
        back_populates="interview_sessions",
    )

    career_recommendation = relationship(
        "CareerRecommendation",
    )

    # -----------------------------------------------------
    # Retry Relationships
    # -----------------------------------------------------

    parent_session = relationship(
        "InterviewSession",
        remote_side=[id],
        foreign_keys=[retry_of_session_id],
        back_populates="retry_sessions",
    )

    retry_sessions = relationship(
        "InterviewSession",
        back_populates="parent_session",
    )

    # -----------------------------------------------------
    # Interview Relationships
    # -----------------------------------------------------

    questions = relationship(
        "InterviewQuestion",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    report = relationship(
        "InterviewReport",
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan",
    )