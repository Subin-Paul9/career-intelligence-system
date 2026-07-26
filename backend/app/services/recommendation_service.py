from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.models.career import Career
from app.models.career_recommendation import CareerRecommendation


def save_recommendation(
    db: Session,
    user_id: int,
    resume_id: int,
    summary: dict,
):
    """
    Save the recommended career and skill gap analysis
    into the recommendations table and create a
    CareerRecommendation record for the interview module.
    """

    # -----------------------------------------
    # Save recommendation history
    # -----------------------------------------

    recommendation = Recommendation(
        user_id=user_id,
        resume_id=resume_id,
        career=summary["recommended_career"],
        match_score=summary["match_score"],
        missing_skills=",".join(summary["improvements"]),
    )

    db.add(recommendation)

    # -----------------------------------------
    # Find Career
    # -----------------------------------------

    career = (
        db.query(Career)
        .filter(
            Career.title == summary["recommended_career"]
        )
        .first()
    )

    if career is None:
        raise ValueError(
            f"Career '{summary['recommended_career']}' not found."
        )

    # -----------------------------------------
    # Save Career Recommendation
    # -----------------------------------------

    career_recommendation = CareerRecommendation(
        user_id=user_id,
        career_id=career.id,
        match_score=summary["match_score"],
    )

    db.add(career_recommendation)

    # -----------------------------------------
    # Commit Transaction
    # -----------------------------------------

    db.commit()

    db.refresh(recommendation)
    db.refresh(career_recommendation)

    return {
        "recommendation": recommendation,
        "career_recommendation": career_recommendation,
    }