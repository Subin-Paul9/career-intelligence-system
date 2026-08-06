from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class VoiceScore(Base):
    __tablename__ = "voice_scores"

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
    # Score Components
    # =====================================================

    technical_score = Column(
        Float,
        nullable=False,
    )

    communication_score = Column(
        Float,
        nullable=False,
    )

    fluency_score = Column(
        Float,
        nullable=False,
    )

    confidence_score = Column(
        Float,
        nullable=False,
    )

    # =====================================================
    # Final Score
    # =====================================================

    overall_score = Column(
        Float,
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
        back_populates="voice_score",
    )