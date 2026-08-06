from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Technical Evaluation
# =====================================================

class TechnicalEvaluationResponse(BaseModel):
    technical_score: float

    strengths: list[str]

    weaknesses: list[str]

    improvement_suggestions: list[str]

    gemini_feedback: str

    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
    )