from sqlalchemy.orm import Session

from app.data.learning_resource_catalog import (
    LEARNING_RESOURCE_CATALOG,
)
from app.services.skill_gap_service import identify_skill_gaps


DIFFICULTY_ORDER = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3,
}


class LearningRecommendationService:
    """
    Recommend learning resources based on missing skills.
    """

    def recommend_resources(
        self,
        missing_skills: list[str],
    ) -> list[dict]:
        """
        Recommend learning resources that match
        the user's missing skills.
        """

        normalized_missing_skills = {
            skill.strip().lower()
            for skill in missing_skills
        }

        recommendations = []

        for resource in LEARNING_RESOURCE_CATALOG:

            if (
                resource["skill"].lower()
                not in normalized_missing_skills
            ):
                continue

            recommendations.append(
                {
                    "skill": resource["skill"],
                    "title": resource["title"],
                    "provider": resource["provider"],
                    "type": resource["type"],
                    "difficulty": resource["difficulty"],
                    "url": resource["url"],
                }
            )

        recommendations.sort(
            key=lambda resource: (
                DIFFICULTY_ORDER.get(
                    resource["difficulty"],
                    999,
                ),
                resource["title"],
            )
        )

        return recommendations


# ---------------------------------------------------
# Backward Compatibility for Phase 5
# ---------------------------------------------------

def recommend_learning_resources(
    db: Session,
    career_title: str,
    resume_skills: list[str],
) -> list[dict]:
    """
    Legacy wrapper used by the Phase 5 Career Summary
    service. It converts resume skills into missing
    skills before recommending learning resources.
    """

    gaps = identify_skill_gaps(
        db=db,
        career_title=career_title,
        resume_skills=resume_skills,
    )

    service = LearningRecommendationService()

    return service.recommend_resources(
        missing_skills=gaps["missing_skills"],
    )