from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Voice Score
# =====================================================

class VoiceScoreResponse(BaseModel):
    technical_score: float

    communication_score: float

    fluency_score: float

    confidence_score: float

    overall_score: float

    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
    )