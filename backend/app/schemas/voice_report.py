from pydantic import BaseModel, ConfigDict


# =====================================================
# Voice Interview Report
# =====================================================

class VoiceInterviewReportResponse(BaseModel):
    # ---------------------------------------------
    # Transcript
    # ---------------------------------------------

    transcript: str

    # ---------------------------------------------
    # Scores
    # ---------------------------------------------

    technical_score: float

    communication_score: float

    fluency_score: float

    confidence_score: float

    overall_score: float

    # ---------------------------------------------
    # AI Feedback
    # ---------------------------------------------

    technical_feedback: str

    strengths: list[str]

    weaknesses: list[str]

    missing_concepts: list[str]

    suggested_practice: list[str]

    learning_resources: list[str]

    model_config = ConfigDict(
        from_attributes=True,
    )