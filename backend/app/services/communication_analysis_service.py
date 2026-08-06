from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.interview_audio import InterviewAudio
from app.models.speech_transcript import SpeechTranscript
from app.models.communication_score import CommunicationScore
from app.schemas.voice_interview import CommunicationScoreResponse


class CommunicationAnalysisService:
    """
    Service responsible for:

    - Loading transcripts
    - Calculating communication metrics
    - Saving communication scores
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
    ) -> tuple[SpeechTranscript, InterviewAudio]:
        """
        Load the transcript and its associated audio.
        """

        transcript = (
            self.db.query(SpeechTranscript)
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

        audio = transcript.audio

        if audio is None:
            raise HTTPException(
                status_code=404,
                detail="Interview audio not found.",
            )

        return (
            transcript,
            audio,
        )

    # =====================================================
    # Calculate Words Per Minute
    # =====================================================

    def calculate_words_per_minute(
        self,
        transcript: SpeechTranscript,
        audio: InterviewAudio,
    ) -> float:
        """
        Calculate the speaker's words per minute (WPM).
        """

        if (
            audio.duration is None
            or audio.duration <= 0
        ):
            return 0.0

        word_count = len(
            transcript.transcript.split()
        )

        words_per_minute = (
            word_count * 60
        ) / audio.duration

        return round(
            words_per_minute,
            2,
        )

    # =====================================================
    # Calculate Pace Score
    # =====================================================

    def calculate_pace_score(
        self,
        words_per_minute: float,
    ) -> float:
        """
        Calculate the speaking pace score based on
        words per minute.
        """

        if words_per_minute <= 0:
            return 0.0

        # Excellent pace
        if 90 <= words_per_minute <= 140:
            return 95.0

        # Good pace
        if 141 <= words_per_minute <= 170:
            return 85.0

        # Slightly fast
        if 171 <= words_per_minute <= 190:
            return 75.0

        # Too fast
        if words_per_minute > 190:
            return 65.0

        # Slightly slow
        if 70 <= words_per_minute < 90:
            return 80.0

        # Too slow
        return 60.0

    # =====================================================
    # Calculate Fluency Score
    # =====================================================

    def calculate_fluency_score(
        self,
        transcript: SpeechTranscript,
    ) -> float:
        """
        Calculate the speaker's fluency score based on
        filler words and repeated words.
        """

        text = transcript.transcript.lower()

        words = text.split()

        total_words = len(words)

        if total_words == 0:
            return 0.0

        # ---------------------------------------------
        # Common filler words
        # ---------------------------------------------

        filler_words = {
            "uh",
            "um",
            "like",
            "actually",
            "basically",
            "literally",
            "okay",
            "well",
        }

        filler_count = sum(
            1
            for word in words
            if word in filler_words
        )

        # ---------------------------------------------
        # Count repeated consecutive words
        # Example:
        # "I I think"
        # ---------------------------------------------

        repeated_count = 0

        for i in range(1, total_words):
            if words[i] == words[i - 1]:
                repeated_count += 1

        # ---------------------------------------------
        # Calculate Penalty
        # ---------------------------------------------

        penalty = (
            filler_count * 2
        ) + (
            repeated_count * 3
        )

        score = max(
            0.0,
            100.0 - penalty,
        )

        return round(
            score,
            2,
        )

    # =====================================================
    # Calculate Clarity Score
    # =====================================================

    def calculate_clarity_score(
        self,
        transcript: SpeechTranscript,
    ) -> float:
        """
        Calculate the speaker's clarity score based on
        sentence structure and word quality.
        """

        text = transcript.transcript.strip()

        if not text:
            return 0.0

        words = text.split()

        total_words = len(words)

        if total_words == 0:
            return 0.0

        # ---------------------------------------------
        # Average Word Length
        # ---------------------------------------------

        average_word_length = (
            sum(len(word.strip(".,!?")) for word in words)
            / total_words
        )

        # ---------------------------------------------
        # Sentence Count
        # ---------------------------------------------

        sentence_count = max(
            1,
            text.count(".")
            + text.count("!")
            + text.count("?"),
        )

        average_sentence_length = (
            total_words / sentence_count
        )

        # ---------------------------------------------
        # Initial Score
        # ---------------------------------------------

        score = 100.0

        # Penalize extremely short words
        if average_word_length < 3:
            score -= 20

        # Penalize extremely long sentences
        if average_sentence_length > 30:
            score -= 15

        # Penalize extremely short sentences
        if average_sentence_length < 5:
            score -= 10

        return max(
            0.0,
            round(score, 2),
        )

    # =====================================================
    # Calculate Overall Score
    # =====================================================

    def calculate_overall_score(
        self,
        clarity_score: float,
        fluency_score: float,
        pace_score: float,
    ) -> float:
        """
        Calculate the overall communication score.
        """

        overall_score = (
            clarity_score
            + fluency_score
            + pace_score
        ) / 3

        return round(
            overall_score,
            2,
        )

    # =====================================================
    # Save Communication Score
    # =====================================================

    def save_score(
        self,
        transcript: SpeechTranscript,
        clarity_score: float,
        fluency_score: float,
        pace_score: float,
        overall_score: float,
    ) -> CommunicationScore:
        """
        Save the communication analysis results.
        """

        # ---------------------------------------------
        # Check Existing Score
        # ---------------------------------------------

        existing = (
            self.db.query(CommunicationScore)
            .filter(
                CommunicationScore.transcript_id
                == transcript.id
            )
            .first()
        )

        if existing is not None:
            return existing

        # ---------------------------------------------
        # Create Communication Score
        # ---------------------------------------------

        communication_score = CommunicationScore(
            transcript_id=transcript.id,
            clarity_score=clarity_score,
            fluency_score=fluency_score,
            pace_score=pace_score,

            # Temporary values
            grammar_score=clarity_score,
            filler_word_score=fluency_score,

            overall_score=overall_score,
        )

        try:

            self.db.add(
                communication_score
            )

            self.db.commit()

            self.db.refresh(
                communication_score
            )

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to save communication score.",
            ) from e

        return communication_score

    # =====================================================
    # Analyze Communication
    # =====================================================

    def analyze(
        self,
        transcript_id: int,
    ) -> CommunicationScoreResponse:
        """
        Analyze a transcript and generate communication scores.
        """

        # ---------------------------------------------
        # Load Transcript
        # ---------------------------------------------

        transcript, audio = self.load_transcript(
            transcript_id=transcript_id,
        )

        # ---------------------------------------------
        # Check Existing Score
        # ---------------------------------------------

        existing = (
            self.db.query(CommunicationScore)
            .filter(
                CommunicationScore.transcript_id
                == transcript.id
            )
            .first()
        )

        if existing is not None:
            return CommunicationScoreResponse(
                clarity_score=existing.clarity_score,
                fluency_score=existing.fluency_score,
                pace_score=existing.pace_score,
                grammar_score=existing.grammar_score,
                filler_word_score=existing.filler_word_score,
                overall_score=existing.overall_score,
                created_at=existing.created_at,
            )

        # ---------------------------------------------
        # Calculate Metrics
        # ---------------------------------------------

        words_per_minute = self.calculate_words_per_minute(
            transcript=transcript,
            audio=audio,
        )

        pace_score = self.calculate_pace_score(
            words_per_minute,
        )

        fluency_score = self.calculate_fluency_score(
            transcript,
        )

        clarity_score = self.calculate_clarity_score(
            transcript,
        )

        overall_score = self.calculate_overall_score(
            clarity_score=clarity_score,
            fluency_score=fluency_score,
            pace_score=pace_score,
        )

        # ---------------------------------------------
        # Save Score
        # ---------------------------------------------

        communication_score = self.save_score(
            transcript=transcript,
            clarity_score=clarity_score,
            fluency_score=fluency_score,
            pace_score=pace_score,
            overall_score=overall_score,
        )

        # ---------------------------------------------
        # Return Response
        # ---------------------------------------------

        return CommunicationScoreResponse(
            clarity_score=communication_score.clarity_score,
            fluency_score=communication_score.fluency_score,
            pace_score=communication_score.pace_score,
            grammar_score=communication_score.grammar_score,
            filler_word_score=communication_score.filler_word_score,
            overall_score=communication_score.overall_score,
            created_at=communication_score.created_at,
        )