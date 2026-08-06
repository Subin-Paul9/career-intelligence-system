from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class SpeechTranscript(Base):
    __tablename__ = "speech_transcripts"

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

    transcript = Column(
        Text,
        nullable=False,
    )

    language = Column(
        String(20),
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

    audio = relationship(
        "InterviewAudio",
        back_populates="transcript",
    )

    communication_score = relationship(
        "CommunicationScore",
        back_populates="transcript",
        uselist=False,
        cascade="all, delete-orphan",
    )

    filler_word_analysis = relationship(
        "FillerWordAnalysis",
        back_populates="transcript",
        uselist=False,
        cascade="all, delete-orphan",
    )

    pronunciation_analysis = relationship(
        "PronunciationAnalysis",
        back_populates="transcript",
        uselist=False,
        cascade="all, delete-orphan",
    )

    technical_evaluation = relationship(
        "TechnicalEvaluation",
        back_populates="transcript",
        uselist=False,
        cascade="all, delete-orphan",
    )

    voice_score = relationship(
        "VoiceScore",
        back_populates="transcript",
        uselist=False,
        cascade="all, delete-orphan",
    )