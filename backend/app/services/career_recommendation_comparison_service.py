from app.data.career_comparison_catalog import (
    CAREER_COMPARISON_CATALOG,
)


class CareerRecommendationComparisonService:
    """
    Generates career comparison data for the
    user's recommended career.

    Used by:
        GET /api/assistant/compare-careers
    """

    def compare(
        self,
        career: str |None,
        match_score: int | None,
    ) -> dict:
        """
        Compare the user's recommended career with
        alternative careers.
        """

        # -------------------------
        # No Recommendation
        # -------------------------
        if not career:
            return {
                "recommended": {
                    "career": "Unknown",
                    "match_score": 0,
                },
                "alternatives": [],
            }

        response = {
            "recommended": {
                "career": career,
                "match_score": match_score or 0,
            },
            "alternatives": [],
        }

        # -------------------------
        # No comparison available
        # -------------------------
        if career not in CAREER_COMPARISON_CATALOG:
            return response

        alternatives = []

        base_score = match_score or 80

        # -------------------------
        # Build alternative careers
        # -------------------------
        for item in CAREER_COMPARISON_CATALOG[
            career
        ]["alternatives"]:

            similarity = item.get(
                "similarity",
                100,
            )

            alternative_score = int(
                round(
                    base_score * similarity / 100
                )
            )

            alternatives.append(
                {
                    "career": item["career"],
                    "match_score": alternative_score,
                    "pros": item["pros"],
                    "cons": item["cons"],
                }
            )

        response["alternatives"] = alternatives

        return response