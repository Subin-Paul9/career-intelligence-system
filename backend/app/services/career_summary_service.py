from sqlalchemy.orm import Session

from app.services.career_recommender import recommend_careers
from app.services.learning_recommendation_service import (
    recommend_learning_resources
)


def generate_career_summary(
    db: Session,
    resume_skills: list[str]
):
    """
    Generate an AI-style career summary.
    """

    # Get ranked careers
    careers = recommend_careers(
        db=db,
        resume_skills=resume_skills
    )

    if not careers:
        return {
            "message": "No suitable career found."
        }

    # Best career
    best = careers[0]

    # Learning recommendations
    learning = recommend_learning_resources(
        db=db,
        career_title=best["career"],
        resume_skills=resume_skills
    )

    strengths = sorted([
        skill
        for skill in best["matched_skills"]
    ])

    improvements = sorted([
        skill
        for skill in best["missing_skills"]
    ])

    summary = (
        f"Based on your resume, you are best suited for "
        f"{best['career']}."
    )

    return {
        "summary": summary,
        "recommended_career": best["career"],
        "match_score": best["match_score"],
        "strengths": strengths,
        "improvements": improvements,
        "learning_resources": learning
    }