from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class FillerWordAnalysis(Base):
    __tablename__ = "filler_word_analyses"

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

    total_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    detected_words = Column(
        JSONB,
        nullable=False,
        default=dict,
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
        back_populates="filler_word_analysis",
    )