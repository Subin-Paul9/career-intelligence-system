from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecommendationRequest(BaseModel):
    resume_id: int


class RecommendationResponse(BaseModel):
    career: str
    match_score: float
    strengths: list[str]
    improvements: list[str]
    learning_resources: list[dict]
    summary: str


class RecommendationHistoryResponse(BaseModel):
    id: int
    resume_id: int
    career: str
    match_score: float
    missing_skills: str | None = None
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CareerDetailsResponse(BaseModel):
    id: int
    title: str
    description: str
    average_salary: str | None = None
    experience_level: str
    required_skills: list[str]

    model_config = ConfigDict(from_attributes=True)