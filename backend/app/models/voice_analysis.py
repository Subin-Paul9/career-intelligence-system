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


class VoiceAnalysis(Base):
    __tablename__ = "voice_analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    audio_id = Column(
        Integer,
        ForeignKey(
            "interview_audios.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    # =====================================================
    # Voice Metrics
    # =====================================================

    speech_duration = Column(
        Float,
        nullable=False,
    )

    silence_duration = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    words_per_minute = Column(
        Float,
        nullable=False,
    )

    pause_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    long_pause_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    average_pause = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    longest_pause = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    speaking_consistency = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================

    audio = relationship(
        "InterviewAudio",
        back_populates="voice_analysis",
    )