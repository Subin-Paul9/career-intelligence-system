from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Voice Upload
# =====================================================

class VoiceUploadRequest(BaseModel):
    answer_id: int


class VoiceUploadResponse(BaseModel):
    audio_id: int

    answer_id: int

    file_name: str

    file_size: int

    duration: Optional[float] = None

    audio_format: str

    message: str

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Speech Transcript
# =====================================================

class TranscriptResponse(BaseModel):
    transcript_id: int

    transcript: str

    language: str

    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Filler Word Detection
# =====================================================

class FillerWordResponse(BaseModel):
    total_count: int

    detected_words: dict[str, int]

    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Communication Score
# =====================================================

class CommunicationScoreResponse(BaseModel):
    clarity_score: float

    fluency_score: float

    pace_score: float

    grammar_score: float

    filler_word_score: float

    overall_score: float

    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Voice Analysis
# =====================================================

class VoiceAnalysisResponse(BaseModel):
    speech_duration: float

    silence_duration: float

    words_per_minute: float

    pause_count: int

    long_pause_count: int

    average_pause: float

    longest_pause: float

    speaking_consistency: float

    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Pronunciation Analysis
# =====================================================

class PronunciationResponse(BaseModel):
    speech_confidence: float

    repeated_word_count: int

    hesitation_count: int

    long_pause_count: int

    overall_pronunciation: float

    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Voice Interview Report
# =====================================================

class VoiceReportResponse(BaseModel):
    upload: VoiceUploadResponse

    transcript: TranscriptResponse

    filler_words: FillerWordResponse

    communication_score: CommunicationScoreResponse

    voice_analysis: VoiceAnalysisResponse

    pronunciation: PronunciationResponse

    model_config = ConfigDict(from_attributes=True)