from sqlalchemy.orm import Session

from app.utils.skill_matcher import match_skills


def identify_skill_gaps(
    db: Session,
    career_title: str,
    resume_skills: list[str]
):
    """
    Identify missing skills required for a career.
    """

    result = match_skills(
        db=db,
        career_title=career_title,
        resume_skills=resume_skills
    )

    return {
        "career": result["career"],
        "missing_skills": result["missing_skills"]
    }