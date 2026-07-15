from sqlalchemy.orm import Session

from app.models.career import Career
from app.utils.skill_matcher import match_skills


def recommend_careers(
    db: Session,
    resume_skills: list[str],
    top_n: int = 5
):
    """
    Recommend the best matching careers
    for the given resume skills.
    """

    careers = db.query(Career).all()

    recommendations = []

    for career in careers:

        result = match_skills(
            db=db,
            career_title=career.title,
            resume_skills=resume_skills
        )

        recommendations.append(result)

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return recommendations[:top_n]