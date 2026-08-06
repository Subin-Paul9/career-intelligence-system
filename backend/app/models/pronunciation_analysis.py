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


class PronunciationAnalysis(Base):
    __tablename__ = "pronunciation_analyses"

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

    speech_confidence = Column(
        Float,
        nullable=False,
    )

    repeated_word_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    hesitation_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    long_pause_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    overall_pronunciation = Column(
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
        back_populates="pronunciation_analysis",
    )