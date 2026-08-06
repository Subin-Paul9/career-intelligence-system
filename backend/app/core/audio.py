"""
Audio Processing Configuration

This module provides reusable audio transcription
services using Faster-Whisper.

Responsibilities:
- Load the Whisper model only once.
- Transcribe audio files.
- Return structured transcription results.
"""

import logging

from faster_whisper import WhisperModel

from app.config.settings import WHISPER_MODEL

logger = logging.getLogger(__name__)


# =====================================================
# Whisper Model Initialization
# =====================================================

logger.info(
    "Loading Whisper model: %s",
    WHISPER_MODEL,
)

try:
    whisper_model = WhisperModel(
        WHISPER_MODEL,
        device="cpu",
        compute_type="int8",
    )

    logger.info(
        "Whisper model loaded successfully."
    )

except Exception:
    logger.exception(
        "Failed to initialize Whisper model."
    )
    raise


# =====================================================
# Audio Transcription
# =====================================================

def transcribe_audio(audio_path: str) -> dict:
    """
    Transcribe an audio file using Faster-Whisper.

    Args:
        audio_path:
            Path to the audio file.

    Returns:
        Dictionary containing:
            - transcript
            - language
            - duration
    """

    logger.info(
        "Transcribing audio: %s",
        audio_path,
    )

    try:

        segments, info = whisper_model.transcribe(
            audio_path,
        )

        transcript = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        logger.info(
            "Audio transcription completed successfully."
        )

        return {
            "transcript": transcript,
            "language": info.language,
            "duration": info.duration,
        }

    except Exception:
        logger.exception(
            "Audio transcription failed."
        )
        raise