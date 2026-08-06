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


class CommunicationScore(Base):
    __tablename__ = "communication_scores"

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

    clarity_score = Column(
        Float,
        nullable=False,
    )

    fluency_score = Column(
        Float,
        nullable=False,
    )

    pace_score = Column(
        Float,
        nullable=False,
    )

    grammar_score = Column(
        Float,
        nullable=False,
    )

    filler_word_score = Column(
        Float,
        nullable=False,
    )

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
        back_populates="communication_score",
    )