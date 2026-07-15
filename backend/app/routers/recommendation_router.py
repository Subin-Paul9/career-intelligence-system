from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.resume import Resume
from app.models.user import User
from app.models.recommendation import Recommendation
from app.models.career import Career
from app.models.skill import Skill
from app.models.career_skill import CareerSkill

from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationHistoryResponse,
    CareerDetailsResponse,
)

from app.services.career_summary_service import generate_career_summary
from app.services.recommendation_service import save_recommendation

from app.utils.skill_extractor import extract_skills


router = APIRouter(
    prefix="/api/career",
    tags=["Career Recommendation"],
)


# =====================================================
# Generate Career Recommendation
# =====================================================
@router.post(
    "/recommend",
    response_model=RecommendationResponse,
    summary="Generate Career Recommendation",
)
def recommend_career(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate career recommendations from a parsed resume,
    save the recommendation to PostgreSQL,
    and return the recommendation summary.
    """

    # Fetch Resume
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    # Ensure resume has been parsed
    if not resume.resume_text:
        raise HTTPException(
            status_code=400,
            detail="Please parse the resume first."
        )

    # Extract skills
    extracted = extract_skills(resume.resume_text)

    resume_skills = []

    for skills in extracted.values():
        resume_skills.extend(skills)

    # Remove duplicates
    resume_skills = list(dict.fromkeys(resume_skills))

    if not resume_skills:
        raise HTTPException(
            status_code=400,
            detail="No skills were found in the resume."
        )

    # Generate recommendation
    summary = generate_career_summary(
        db=db,
        resume_skills=resume_skills,
    )

    # Save recommendation
    save_recommendation(
        db=db,
        user_id=current_user.id,
        resume_id=resume.id,
        summary=summary,
    )

    # Return response
    return RecommendationResponse(
        career=summary["recommended_career"],
        match_score=summary["match_score"],
        strengths=summary["strengths"],
        improvements=summary["improvements"],
        learning_resources=summary["learning_resources"],
        summary=summary["summary"],
    )


# =====================================================
# Recommendation History
# =====================================================
@router.get(
    "/history",
    response_model=list[RecommendationHistoryResponse],
    summary="Recommendation History",
)
def get_recommendation_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all previous career recommendations
    generated for the logged-in user.
    """

    recommendations = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == current_user.id
        )
        .order_by(
            Recommendation.generated_at.desc()
        )
        .all()
    )

    return recommendations


# =====================================================
# Career Details
# =====================================================
@router.get(
    "/{career_id}",
    response_model=CareerDetailsResponse,
    summary="Career Details",
)
def get_career_details(
    career_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return detailed information about a career.
    """

    career = (
        db.query(Career)
        .filter(Career.id == career_id)
        .first()
    )

    if not career:
        raise HTTPException(
            status_code=404,
            detail="Career not found."
        )

    required_skills = (
        db.query(Skill.name)
        .join(
            CareerSkill,
            Skill.id == CareerSkill.skill_id
        )
        .filter(
            CareerSkill.career_id == career.id
        )
        .all()
    )

    skills = [skill[0] for skill in required_skills]

    return CareerDetailsResponse(
        id=career.id,
        title=career.title,
        description=career.description,
        average_salary=career.average_salary,
        experience_level=career.experience_level,
        required_skills=skills,
    )