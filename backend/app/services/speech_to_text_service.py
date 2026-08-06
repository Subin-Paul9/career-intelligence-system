from pathlib import Path

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.audio import transcribe_audio
from app.models.interview_audio import InterviewAudio
from app.models.speech_transcript import SpeechTranscript
from app.schemas.voice_interview import TranscriptResponse


class SpeechToTextService:
    """
    Service responsible for:

    - Loading interview audio
    - Generating speech transcripts
    - Saving transcripts
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Load Audio
    # =====================================================

    def load_audio(
        self,
        audio_id: int,
    ) -> InterviewAudio:
        """
        Load an interview audio record from the database.
        """

        audio = (
            self.db.query(InterviewAudio)
            .filter(
                InterviewAudio.id == audio_id
            )
            .first()
        )

        if audio is None:
            raise HTTPException(
                status_code=404,
                detail="Interview audio not found.",
            )

        audio_path = Path(audio.file_path)

        if not audio_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Audio file not found on disk.",
            )

        return audio

    # =====================================================
    # Transcribe Audio
    # =====================================================

    def transcribe_audio_file(
        self,
        audio: InterviewAudio,
    ) -> dict:
        """
        Generate a speech transcript using Faster-Whisper.
        """

        try:
            result = transcribe_audio(
                audio.file_path,
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Failed to transcribe audio.",
            ) from e

        if not result.get("transcript"):
            raise HTTPException(
                status_code=500,
                detail="Whisper returned an empty transcript.",
            )

        return result

    # =====================================================
    # Save Transcript
    # =====================================================

    def save_transcript(
        self,
        audio_id: int,
        transcript: str,
        language: str,
    ) -> SpeechTranscript:
        """
        Save the generated transcript to the database.
        """

        # ---------------------------------------------
        # Check Existing Transcript
        # ---------------------------------------------

        existing = (
            self.db.query(SpeechTranscript)
            .filter(
                SpeechTranscript.audio_id == audio_id
            )
            .first()
        )

        if existing is not None:
            return existing

        # ---------------------------------------------
        # Create Transcript
        # ---------------------------------------------

        speech_transcript = SpeechTranscript(
            audio_id=audio_id,
            transcript=transcript,
            language=language,
        )

        try:
            self.db.add(
                speech_transcript
            )

            self.db.commit()

            self.db.refresh(
                speech_transcript
            )

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to save transcript.",
            ) from e

        return speech_transcript

    # =====================================================
    # Generate Transcript
    # =====================================================

    def generate_transcript(
        self,
        audio_id: int,
    ) -> TranscriptResponse:
        """
        Generate and save a transcript for an interview audio.
        """

        # ---------------------------------------------
        # Load Audio
        # ---------------------------------------------

        audio = self.load_audio(
            audio_id=audio_id,
        )

        # ---------------------------------------------
        # Check Existing Transcript
        # ---------------------------------------------

        existing = (
            self.db.query(SpeechTranscript)
            .filter(
                SpeechTranscript.audio_id == audio.id
            )
            .first()
        )

        if existing is not None:
            return TranscriptResponse(
                transcript_id=existing.id,
                transcript=existing.transcript,
                language=existing.language,
                created_at=existing.created_at,
            )

        # ---------------------------------------------
        # Generate Transcript
        # ---------------------------------------------

        result = self.transcribe_audio_file(
            audio,
        )

        # ---------------------------------------------
        # Update Audio Duration
        # ---------------------------------------------

        audio.duration = result.get(
            "duration",
            audio.duration,
        )

        try:
            self.db.commit()

            self.db.refresh(audio)

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to update audio duration.",
            ) from e

        # ---------------------------------------------
        # Save Transcript
        # ---------------------------------------------

        transcript = self.save_transcript(
            audio_id=audio.id,
            transcript=result["transcript"],
            language=result["language"],
        )

        # ---------------------------------------------
        # Return Response
        # ---------------------------------------------

        return TranscriptResponse(
            transcript_id=transcript.id,
            transcript=transcript.transcript,
            language=transcript.language,
            created_at=transcript.created_at,
        )

    # =====================================================
    # Get Transcript
    # =====================================================

    def get_transcript(
        self,
        audio_id: int,
    ) -> TranscriptResponse:
        """
        Retrieve an existing transcript
        for an interview audio.
        """

        transcript = (
            self.db.query(
                SpeechTranscript,
            )
            .filter(
                SpeechTranscript.audio_id
                == audio_id,
            )
            .first()
        )

        if transcript is None:
            raise HTTPException(
                status_code=404,
                detail="Transcript not found.",
            )

        return TranscriptResponse(
            transcript_id=transcript.id,
            transcript=transcript.transcript,
            language=transcript.language,
            created_at=transcript.created_at,
        )