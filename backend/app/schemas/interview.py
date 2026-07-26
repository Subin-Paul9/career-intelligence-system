from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# =====================================================
# Enums
# =====================================================

class DifficultyEnum(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


# =====================================================
# Start Interview
# =====================================================

class InterviewStartRequest(BaseModel):
    career_recommendation_id: Optional[int] = None
    interview_type: str
    difficulty: DifficultyEnum
    total_questions: int = 10


class InterviewStartResponse(BaseModel):
    session_id: int
    question: str

    model_config = ConfigDict(from_attributes=True)


class RetryInterviewResponse(BaseModel):
    session_id: int
    attempt_number: int
    question: str

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Interview Question
# =====================================================

class InterviewQuestionResponse(BaseModel):
    question_id: int
    question_order: int
    question: str
    category: str
    difficulty: str

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Submit Answer
# =====================================================

class InterviewAnswerRequest(BaseModel):
    question_id: int
    answer: str

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Answer cannot be empty.")
        return value


class InterviewAnswerResponse(BaseModel):
    question_id: int
    technical_score: float
    communication_score: float
    confidence_score: float
    overall_score: float
    ai_feedback: str

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Interview Report
# =====================================================

class InterviewReportResponse(BaseModel):
    session_id: int

    technical_score: float
    communication_score: float
    problem_solving_score: float
    confidence_score: float
    overall_score: float

    strengths: str
    weaknesses: str

    ai_summary: str
    recommendation: str

    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Interview History
# =====================================================

class InterviewHistoryResponse(BaseModel):
    session_id: int

    attempt_number: int
    retry_of_session_id: Optional[int] = None

    interview_type: str
    difficulty: str

    overall_score: Optional[float] = None
    status: str

    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Interview Details
# =====================================================

class InterviewQuestionDetailResponse(BaseModel):
    question_id: int
    question_order: int
    question: str
    category: str
    difficulty: str

    answer: Optional[str] = None

    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    confidence_score: Optional[float] = None
    overall_score: Optional[float] = None

    ai_feedback: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class InterviewSessionDetailResponse(BaseModel):
    session_id: int

    attempt_number: int
    retry_of_session_id: Optional[int] = None

    interview_type: str
    difficulty: str
    status: str

    total_questions: int
    answered_questions: int

    overall_score: Optional[float] = None

    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Recommendation
# =====================================================

class RecommendationResponse(BaseModel):
    missing_skills: list[str] = Field(default_factory=list)
    learning_resources: list[str] = Field(default_factory=list)
    suggested_projects: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Interview Report Details
# =====================================================

class InterviewReportDetailResponse(BaseModel):
    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    problem_solving_score: Optional[float] = None
    confidence_score: Optional[float] = None
    overall_score: Optional[float] = None

    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)

    missing_topics: list[str] = Field(default_factory=list)
    learning_resources: list[str] = Field(default_factory=list)
    suggested_projects: list[str] = Field(default_factory=list)

    ai_summary: Optional[str] = None

    recommendation: Optional[RecommendationResponse] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Interview Feedback
# =====================================================

class InterviewFeedbackResponse(BaseModel):
    feedback_id: int

    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)

    missing_skills: list[str] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)
    learning_resources: list[str] = Field(default_factory=list)
    mentor_advice: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class InterviewDetailResponse(BaseModel):
    session: InterviewSessionDetailResponse
    questions: list[InterviewQuestionDetailResponse]
    report: Optional[InterviewReportDetailResponse] = None
    feedback: Optional[InterviewFeedbackResponse] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Delete Interview
# =====================================================

class DeleteInterviewResponse(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)