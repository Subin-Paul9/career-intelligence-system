from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class InterviewAudio(Base):
    __tablename__ = "interview_audios"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    answer_id = Column(
        Integer,
        ForeignKey(
            "interview_answers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    file_name = Column(
        String(255),
        nullable=False,
    )

    file_path = Column(
        String(500),
        nullable=False,
    )

    # Store file size in bytes
    file_size = Column(
        BigInteger,
        nullable=False,
    )

    # Audio duration in seconds
    duration = Column(
        Float,
        nullable=True,
    )

    audio_format = Column(
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

    answer = relationship(
        "InterviewAnswer",
        back_populates="audio",
    )

    transcript = relationship(
        "SpeechTranscript",
        back_populates="audio",
        uselist=False,
        cascade="all, delete-orphan",
    )

    voice_analysis = relationship(
        "VoiceAnalysis",
        back_populates="audio",
        uselist=False,
        cascade="all, delete-orphan",
    )