from app.data.career_mapping import CAREER_MAPPING
from app.data.certification_catalog import (
    CERTIFICATION_CATALOG,
)


DIFFICULTY_ORDER = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3,
}


class CertificationRecommendationService:
    """
    Service responsible for recommending certifications
    based on the user's career path, missing skills,
    and optional difficulty level.
    """

    def recommend_certifications(
        self,
        career: str | None,
        missing_skills: list[str],
        difficulty: str | None = None,
    ) -> list[dict]:
        """
        Recommend certifications that best match the
        user's career path and missing skills.

        Parameters
        ----------
        career:
            Recommended career path.

        missing_skills:
            Skills the user needs to improve.

        difficulty:
            Optional difficulty filter
            (Beginner, Intermediate, Advanced).

        Returns
        -------
        list[dict]
            A list of recommended certifications sorted
            by relevance and difficulty.
        """

        recommendations = []

        # ----------------------------------------
        # Resolve career mapping
        # ----------------------------------------
        if career:
            careers = CAREER_MAPPING.get(
                career,
                [career],
            )
        else:
            careers = []

        # ----------------------------------------
        # Normalize missing skills
        # ----------------------------------------
        normalized_missing_skills = {
            skill.strip().lower()
            for skill in missing_skills
        }

        # ----------------------------------------
        # Recommend certifications
        # ----------------------------------------
        for certification in CERTIFICATION_CATALOG:

            # Filter by mapped careers
            if careers:
                if certification["career"] not in careers:
                    continue

            # Filter by difficulty (optional)
            if (
                difficulty
                and certification["difficulty"].lower()
                != difficulty.lower()
            ):
                continue

            # Find matching skills
            matched_skills = [
                skill
                for skill in certification["skills"]
                if skill.lower() in normalized_missing_skills
            ]

            recommendations.append(
                {
                    "name": certification["name"],
                    "provider": certification["provider"],
                    "career": certification["career"],
                    "difficulty": certification["difficulty"],
                    "description": certification["description"],
                    "skills": certification["skills"],
                    "matched_skills": matched_skills,
                    "match_score": len(matched_skills),
                    "url": certification["url"],
                }
            )

        # ----------------------------------------
        # Sort recommendations
        # ----------------------------------------
        recommendations.sort(
            key=lambda certification: (
                -certification["match_score"],
                DIFFICULTY_ORDER.get(
                    certification["difficulty"],
                    999,
                ),
            )
        )

        return recommendations