from copy import deepcopy

from app.data.roadmap_catalog import ROADMAP_CATALOG


class RoadmapGeneratorService:
    """
    Generates a personalized 30/60/90-day roadmap
    based on the user's recommended career,
    missing skills, and current skills.
    """

    @staticmethod
    def get_roadmap(career: str) -> dict | None:
        """
        Retrieve the roadmap for a given career.

        Supports:
        - Exact matching
        - Partial matching
        """

        if not career:
            return None

        career = career.lower().strip()

        # -------------------------
        # Exact Match
        # -------------------------
        for roadmap in ROADMAP_CATALOG:
            if roadmap["career"].lower() == career:
                return deepcopy(roadmap)

        # -------------------------
        # Partial Match
        # -------------------------
        for roadmap in ROADMAP_CATALOG:
            if career in roadmap["career"].lower():
                return deepcopy(roadmap)

        return None

    def generate_roadmap(
        self,
        career: str,
        missing_skills: list[str] | None,
        current_skills: list[str] | None,
    ) -> dict:
        """
        Generate a personalized roadmap.

        Rules:
        - Remove skills the user already possesses.
        - Prioritize missing skills.
        - Avoid duplicate roadmap items.
        """

        roadmap = self.get_roadmap(career)

        # -------------------------
        # Fallback Roadmap
        # -------------------------
        if roadmap is None:
            return {
                "career": career or "Unknown",
                "day_30": [],
                "day_60": [],
                "day_90": [],
            }

        missing_skills = missing_skills or []
        current_skills = current_skills or []

        current_skills_lower = {
            skill.lower()
            for skill in current_skills
        }

        # -------------------------
        # Remove Existing Skills
        # -------------------------
        for phase in (
            "day_30",
            "day_60",
            "day_90",
        ):
            roadmap[phase] = [
                item
                for item in roadmap[phase]
                if item.lower() not in current_skills_lower
            ]

        # -------------------------
        # Existing Roadmap Items
        # -------------------------
        roadmap_items = {
            item.lower()
            for phase in (
                "day_30",
                "day_60",
                "day_90",
            )
            for item in roadmap[phase]
        }

        # -------------------------
        # Prioritize Missing Skills
        # -------------------------
        for skill in reversed(missing_skills):
            normalized_skill = skill.strip()

            if normalized_skill.lower() not in roadmap_items:
                roadmap["day_30"].insert(
                    0,
                    normalized_skill,
                )
                roadmap_items.add(
                    normalized_skill.lower()
                )

        return roadmap