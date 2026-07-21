from pydantic import BaseModel


class QuestionsResponse(BaseModel):
    questions: list[str]


class ProjectResponse(BaseModel):
    title: str
    career: str
    difficulty: str
    description: str
    skills: list[str]
    matched_skills: list[str]
    match_score: int


class ProjectsResponse(BaseModel):
    projects: list[ProjectResponse]


class CertificationResponse(BaseModel):
    name: str
    provider: str
    career: str
    difficulty: str
    description: str
    skills: list[str]
    matched_skills: list[str]
    match_score: int
    url: str


class CertificationsResponse(BaseModel):
    certifications: list[CertificationResponse]


class ResourceResponse(BaseModel):
    skill: str
    title: str
    provider: str
    type: str
    difficulty: str
    url: str


class ResourcesResponse(BaseModel):
    resources: list[ResourceResponse]


class RoadmapResponse(BaseModel):
    career: str
    day_30: list[str]
    day_60: list[str]
    day_90: list[str]


class RecommendedCareerResponse(BaseModel):
    career: str
    match_score: int


class CareerComparisonItem(BaseModel):
    career: str
    match_score: int
    pros: list[str]
    cons: list[str]


class CareerComparisonResponse(BaseModel):
    recommended: RecommendedCareerResponse
    alternatives: list[CareerComparisonItem]