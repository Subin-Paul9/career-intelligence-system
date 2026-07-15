import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.services.skill_gap_service import identify_skill_gaps


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATASET = PROJECT_ROOT / "datasets" / "learning_resources.json"


def recommend_learning_resources(
    db: Session,
    career_title: str,
    resume_skills: list[str]
):
    """
    Recommend learning resources for the missing skills.
    """

    gaps = identify_skill_gaps(
        db=db,
        career_title=career_title,
        resume_skills=resume_skills
    )

    with open(DATASET, "r", encoding="utf-8") as file:
        resources = json.load(file)

    recommendations = []

    for skill in gaps["missing_skills"]:

        resource = resources.get(
            skill.lower(),
            {
                "platform": "Google",
                "resource": f"Learn {skill}",
                "url": f"https://www.google.com/search?q={skill}+tutorial"
            }
        )

        recommendations.append({
            "skill": skill,
            "platform": resource["platform"],
            "resource": resource["resource"],
            "url": resource["url"]
        })

    return recommendations