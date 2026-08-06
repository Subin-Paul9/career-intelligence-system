import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.filler_word_analysis import (
    FillerWordAnalysis,
)
from app.models.speech_transcript import (
    SpeechTranscript,
)
from app.schemas.voice_interview import (
    FillerWordResponse,
)


class FillerWordDetectionService:
    """
    Service responsible for:

    - Loading speech transcripts
    - Detecting filler words
    - Counting filler words
    - Saving analysis
    """

    FILLER_WORDS = {
        "um",
        "uh",
        "like",
        "basically",
        "actually",
        "hmm",
    }

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Load Transcript
    # =====================================================

    def load_transcript(
        self,
        transcript_id: int,
    ) -> SpeechTranscript:
        """
        Load a speech transcript from the database.
        """

        transcript = (
            self.db.query(
                SpeechTranscript
            )
            .filter(
                SpeechTranscript.id == transcript_id
            )
            .first()
        )

        if transcript is None:
            raise HTTPException(
                status_code=404,
                detail="Speech transcript not found.",
            )

        return transcript

    # =====================================================
    # Normalize Text
    # =====================================================

    def normalize_text(
        self,
        text: str,
    ) -> str:
        """
        Normalize transcript text for filler word detection.

        Steps:
        - Convert to lowercase.
        - Remove punctuation.
        - Remove extra whitespace.
        """

        if not text:
            return ""

        # ---------------------------------------------
        # Convert to lowercase
        # ---------------------------------------------

        normalized_text = text.lower()

        # ---------------------------------------------
        # Remove punctuation
        # ---------------------------------------------

        normalized_text = re.sub(
            r"[^\w\s]",
            " ",
            normalized_text,
        )

        # ---------------------------------------------
        # Remove extra whitespace
        # ---------------------------------------------

        normalized_text = re.sub(
            r"\s+",
            " ",
            normalized_text,
        ).strip()

        return normalized_text

    # =====================================================
    # Detect Filler Words
    # =====================================================

    def detect_filler_words(
        self,
        normalized_text: str,
    ) -> tuple[int, dict[str, int]]:
        """
        Detect filler words in a normalized transcript.

        Returns:
            (
                total_count,
                detected_words,
            )
        """

        detected_words: dict[str, int] = {}

        total_count = 0

        # ---------------------------------------------
        # Tokenize Transcript
        # ---------------------------------------------

        words = re.findall(r"\b\w+\b", normalized_text)

        # ---------------------------------------------
        # Count Filler Words
        # ---------------------------------------------

        for word in words:

            if word in self.FILLER_WORDS:

                detected_words[word] = (
                    detected_words.get(
                        word,
                        0,
                    )
                    + 1
                )

                total_count += 1

        return (
            total_count,
            detected_words,
        )

    # =====================================================
    # Save Analysis
    # =====================================================

    def save_analysis(
        self,
        transcript_id: int,
        total_count: int,
        detected_words: dict[str, int],
    ) -> FillerWordAnalysis:
        """
        Save the filler word analysis.

        If an analysis already exists, update it.
        Otherwise, create a new one.
        """

        analysis = (
            self.db.query(
                FillerWordAnalysis
            )
            .filter(
                FillerWordAnalysis.transcript_id
                == transcript_id
            )
            .first()
        )

        if analysis is None:

            analysis = FillerWordAnalysis(
                transcript_id=transcript_id,
            )

            self.db.add(
                analysis
            )

        # ---------------------------------------------
        # Update Analysis
        # ---------------------------------------------

        analysis.total_count = total_count

        analysis.detected_words = (
            detected_words
        )

        try:

            self.db.commit()

            self.db.refresh(
                analysis
            )

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail=(
                    "Failed to save filler word analysis."
                ),
            ) from e

        return analysis

    # =====================================================
    # Analyze Filler Words
    # =====================================================

    def analyze(
        self,
        transcript_id: int,
    ) -> FillerWordResponse:
        """
        Analyze a speech transcript for filler words.
        """

        # ---------------------------------------------
        # Load Transcript
        # ---------------------------------------------

        transcript = self.load_transcript(
            transcript_id=transcript_id,
        )

        # ---------------------------------------------
        # Normalize Transcript
        # ---------------------------------------------

        normalized_text = self.normalize_text(
            transcript.transcript or "",
        )

        # ---------------------------------------------
        # Detect Filler Words
        # ---------------------------------------------

        (
            total_count,
            detected_words,
        ) = self.detect_filler_words(
            normalized_text,
        )

        # ---------------------------------------------
        # Save Analysis
        # ---------------------------------------------

        analysis = self.save_analysis(
            transcript_id=transcript.id,
            total_count=total_count,
            detected_words=detected_words,
        )

        # ---------------------------------------------
        # Return Response
        # ---------------------------------------------

        return FillerWordResponse(
            total_count=analysis.total_count,
            detected_words=analysis.detected_words,
            created_at=analysis.created_at,
        )