from datetime import datetime

from pydantic import BaseModel


class VoiceHistoryItemResponse(BaseModel):
    session_id: int
    interview_type: str
    difficulty: str
    answered_questions: int
    total_questions: int
    overall_score: float | None
    completed_at: datetime | None

    class Config:
        from_attributes = True


class VoiceHistoryResponse(BaseModel):
    history: list[VoiceHistoryItemResponse]