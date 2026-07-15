from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation


def save_recommendation(
    db: Session,
    user_id: int,
    resume_id: int,
    summary: dict,
):
    """
    Save the recommended career and skill gap analysis
    into the recommendations table.
    """

    recommendation = Recommendation(
        user_id=user_id,
        resume_id=resume_id,
        career=summary["recommended_career"],
        match_score=summary["match_score"],
        missing_skills=",".join(summary["improvements"]),
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation