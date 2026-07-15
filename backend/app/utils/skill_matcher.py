from sqlalchemy.orm import Session

from app.models.career import Career
from app.models.skill import Skill
from app.models.career_skill import CareerSkill


def match_skills(
    db: Session,
    career_title: str,
    resume_skills: list[str]
):
    """
    Compare resume skills against the required skills
    for a career stored in PostgreSQL.
    """

    # -----------------------------
    # Get career
    # -----------------------------
    career = (
        db.query(Career)
        .filter(Career.title == career_title)
        .first()
    )

    if not career:
        raise ValueError(f"Career '{career_title}' not found.")

    # -----------------------------
    # Get required skills
    # -----------------------------
    required_skills = (
        db.query(Skill.name)
        .join(
            CareerSkill,
            Skill.id == CareerSkill.skill_id
        )
        .filter(CareerSkill.career_id == career.id)
        .all()
    )

    # Convert tuples to list
    required = [skill.name for skill in required_skills]

    # -----------------------------
    # Compare skills
    # -----------------------------
    resume_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    career_set = {
        skill.strip().lower()
        for skill in required
    }

    matched = resume_set & career_set
    missing = career_set - matched

    score = 0.0

    if career_set:
        score = round(
            len(matched) / len(career_set) * 100,
            2
        )

    return {
        "career": career.title,
        "match_score": score,
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
    }


def match_all_careers(
    db: Session,
    resume_skills: list[str]
):
    """
    Compare a resume against every career
    and return results sorted by match score.
    """

    careers = db.query(Career).all()

    results = []

    for career in careers:
        result = match_skills(
            db=db,
            career_title=career.title,
            resume_skills=resume_skills
        )

        results.append(result)

    results.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return results