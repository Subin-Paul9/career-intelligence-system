from datetime import datetime

from pydantic import BaseModel, ConfigDict


# =====================================================
# Career Response
# =====================================================
class CareerResponse(BaseModel):
    id: int
    title: str
    description: str
    average_salary: str | None = None
    experience_level: str

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Skill Response
# =====================================================
class SkillResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Career Recommendation Response
# =====================================================
class RecommendationResponse(BaseModel):
    id: int
    user_id: int
    career_id: int
    match_score: float
    recommended_at: datetime

    model_config = ConfigDict(from_attributes=True)