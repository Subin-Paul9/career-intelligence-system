from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.speech_transcript import (
    SpeechTranscript,
)
from app.models.voice_analysis import (
    VoiceAnalysis,
)
from app.models.filler_word_analysis import (
    FillerWordAnalysis,
)
from app.models.pronunciation_analysis import (
    PronunciationAnalysis,
)
from app.schemas.voice_interview import (
    PronunciationResponse,
)


class PronunciationAnalysisService:
    """
    Service responsible for:

    - Loading transcript
    - Detecting repeated words
    - Calculating hesitation
    - Calculating speech confidence
    - Calculating pronunciation score
    - Saving analysis
    """

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
        Load a speech transcript.
        """

        transcript = (
            self.db.query(
                SpeechTranscript,
            )
            .filter(
                SpeechTranscript.id == transcript_id,
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
    # Load Voice Analysis
    # =====================================================

    def load_voice_analysis(
        self,
        transcript: SpeechTranscript,
    ) -> VoiceAnalysis:
        """
        Load the voice analysis associated with
        the transcript's audio.
        """

        voice_analysis = (
            self.db.query(
                VoiceAnalysis,
            )
            .filter(
                VoiceAnalysis.audio_id
                == transcript.audio_id,
            )
            .first()
        )

        if voice_analysis is None:
            raise HTTPException(
                status_code=404,
                detail="Voice analysis not found.",
            )

        return voice_analysis

    # =====================================================
    # Load Filler Word Analysis
    # =====================================================

    def load_filler_word_analysis(
        self,
        transcript: SpeechTranscript,
    ) -> FillerWordAnalysis:
        """
        Load the filler word analysis associated
        with the transcript.
        """

        filler_word_analysis = (
            self.db.query(
                FillerWordAnalysis,
            )
            .filter(
                FillerWordAnalysis.transcript_id
                == transcript.id,
            )
            .first()
        )

        if filler_word_analysis is None:
            raise HTTPException(
                status_code=404,
                detail="Filler word analysis not found.",
            )

        return filler_word_analysis

    # =====================================================
    # Detect Repeated Words
    # =====================================================

    def detect_repeated_words(
        self,
        transcript: SpeechTranscript,
    ) -> int:
        """
        Detect consecutive repeated words.

        Example:
            "I I think think this is good"

        Returns:
            Number of repeated words.
        """

        text = (
            transcript.transcript or ""
        ).lower()

        words = text.split()

        repeated_word_count = 0

        for index in range(
            1,
            len(words),
        ):

            if (
                words[index]
                == words[index - 1]
            ):

                repeated_word_count += 1

        return repeated_word_count

    # =====================================================
    # Calculate Hesitation
    # =====================================================

    def calculate_hesitation(
        self,
        repeated_word_count: int,
        filler_word_analysis: FillerWordAnalysis,
    ) -> int:
        """
        Calculate the hesitation count.

        Hesitation is estimated using:

        - Repeated words
        - Filler words
        """

        hesitation_count = (
            repeated_word_count
            + filler_word_analysis.total_count
        )

        return hesitation_count

    # =====================================================
    # Calculate Speech Confidence
    # =====================================================

    def calculate_speech_confidence(
        self,
        hesitation_count: int,
        voice_analysis: VoiceAnalysis,
    ) -> float:
        """
        Calculate the speaker's confidence score.

        The score starts at 100 and is reduced
        based on hesitation and pauses.
        """

        confidence = 100.0

        # ---------------------------------------------
        # Hesitation Penalty
        # ---------------------------------------------

        confidence -= (
            hesitation_count * 2
        )

        # ---------------------------------------------
        # Pause Count Penalty
        # ---------------------------------------------

        confidence -= (
            voice_analysis.pause_count * 0.5
        )

        confidence -= (
            voice_analysis.long_pause_count * 2
        )

        # ---------------------------------------------
        # Long Pause Penalty
        # ---------------------------------------------

        if voice_analysis.longest_pause > 2:

            confidence -= (
                (
                    voice_analysis.longest_pause
                    - 2
                )
                * 5
            )

        # ---------------------------------------------
        # Clamp Score
        # ---------------------------------------------

        confidence = max(
            0.0,
            min(
                100.0,
                confidence,
            ),
        )

        return round(
            confidence,
            2,
        )

    # =====================================================
    # Calculate Overall Pronunciation
    # =====================================================

    def calculate_overall_pronunciation(
        self,
        speech_confidence: float,
        voice_analysis: VoiceAnalysis,
    ) -> float:
        """
        Calculate the overall pronunciation score.

        Score Components:
        - Speech Confidence (70%)
        - Speaking Consistency (30%)
        """

        overall_score = (
            speech_confidence * 0.70
            + voice_analysis.speaking_consistency * 0.30
        )

        overall_score = max(
            0.0,
            min(
                100.0,
                overall_score,
            ),
        )

        return round(
            overall_score,
            2,
        )

    # =====================================================
    # Save Analysis
    # =====================================================

    def save_analysis(
        self,
        transcript_id: int,
        speech_confidence: float,
        repeated_word_count: int,
        hesitation_count: int,
        long_pause_count: int,
        overall_pronunciation: float,
    ) -> PronunciationAnalysis:
        """
        Save the pronunciation analysis.

        If an analysis already exists, update it.
        Otherwise, create a new one.
        """

        analysis = (
            self.db.query(
                PronunciationAnalysis,
            )
            .filter(
                PronunciationAnalysis.transcript_id
                == transcript_id,
            )
            .first()
        )

        if analysis is None:

            analysis = PronunciationAnalysis(
                transcript_id=transcript_id,
            )

            self.db.add(
                analysis,
            )

        # ---------------------------------------------
        # Update Analysis
        # ---------------------------------------------

        analysis.speech_confidence = (
            speech_confidence
        )

        analysis.repeated_word_count = (
            repeated_word_count
        )

        analysis.hesitation_count = (
            hesitation_count
        )

        analysis.long_pause_count = (
            long_pause_count
        )

        analysis.overall_pronunciation = (
            overall_pronunciation
        )

        try:

            self.db.commit()

            self.db.refresh(
                analysis,
            )

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail=(
                    "Failed to save pronunciation analysis."
                ),
            ) from e

        return analysis

    # =====================================================
    # Analyze Pronunciation
    # =====================================================

    def analyze(
        self,
        transcript_id: int,
    ) -> PronunciationResponse:
        """
        Analyze pronunciation from a speech transcript.
        """

        # ---------------------------------------------
        # Load Transcript
        # ---------------------------------------------

        transcript = self.load_transcript(
            transcript_id=transcript_id,
        )

        # ---------------------------------------------
        # Load Existing Analyses
        # ---------------------------------------------

        voice_analysis = self.load_voice_analysis(
            transcript=transcript,
        )

        filler_word_analysis = (
            self.load_filler_word_analysis(
                transcript=transcript,
            )
        )

        # ---------------------------------------------
        # Detect Repeated Words
        # ---------------------------------------------

        repeated_word_count = (
            self.detect_repeated_words(
                transcript=transcript,
            )
        )

        # ---------------------------------------------
        # Calculate Hesitation
        # ---------------------------------------------

        hesitation_count = (
            self.calculate_hesitation(
                repeated_word_count=repeated_word_count,
                filler_word_analysis=filler_word_analysis,
            )
        )

        # ---------------------------------------------
        # Calculate Speech Confidence
        # ---------------------------------------------

        speech_confidence = (
            self.calculate_speech_confidence(
                hesitation_count=hesitation_count,
                voice_analysis=voice_analysis,
            )
        )

        # ---------------------------------------------
        # Calculate Overall Pronunciation
        # ---------------------------------------------

        overall_pronunciation = (
            self.calculate_overall_pronunciation(
                speech_confidence=speech_confidence,
                voice_analysis=voice_analysis,
            )
        )

        # ---------------------------------------------
        # Save Analysis
        # ---------------------------------------------

        analysis = self.save_analysis(
            transcript_id=transcript.id,
            speech_confidence=speech_confidence,
            repeated_word_count=repeated_word_count,
            hesitation_count=hesitation_count,
            long_pause_count=voice_analysis.long_pause_count,
            overall_pronunciation=overall_pronunciation,
        )

        # ---------------------------------------------
        # Return Response
        # ---------------------------------------------

        return PronunciationResponse(
            speech_confidence=analysis.speech_confidence,
            repeated_word_count=analysis.repeated_word_count,
            hesitation_count=analysis.hesitation_count,
            long_pause_count=analysis.long_pause_count,
            overall_pronunciation=analysis.overall_pronunciation,
            created_at=analysis.created_at,
        )