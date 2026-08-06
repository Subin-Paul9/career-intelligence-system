from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class TechnicalEvaluation(Base):
    __tablename__ = "technical_evaluations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    transcript_id = Column(
        Integer,
        ForeignKey(
            "speech_transcripts.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    # =====================================================
    # Technical Evaluation Metrics
    # =====================================================

    technical_score = Column(
        Float,
        nullable=False,
    )

    strengths = Column(
        JSONB,
        nullable=False,
        default=list,
    )

    weaknesses = Column(
        JSONB,
        nullable=False,
        default=list,
    )

    improvement_suggestions = Column(
        JSONB,
        nullable=False,
        default=list,
    )

    gemini_feedback = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================

    transcript = relationship(
        "SpeechTranscript",
        back_populates="technical_evaluation",
    )