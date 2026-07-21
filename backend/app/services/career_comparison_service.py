from app.data.career_catalog import CAREER_CATALOG


class CareerComparisonService:
    """
    Provides career comparison functionality.
    """

    @staticmethod
    def get_career(name: str) -> dict | None:
        """
        Find a career by name.

        Supports both exact and partial matching.
        """

        search = name.strip().lower()

        # Exact match
        for career in CAREER_CATALOG:
            if career["name"].lower() == search:
                return career

        # Partial match
        for career in CAREER_CATALOG:
            if search in career["name"].lower():
                return career

        return None

    @staticmethod
    def extract_careers(question: str) -> list[str]:
        """
        Extract career names mentioned in the user's question.
        """

        question = question.lower()
        careers: list[str] = []

        for career in CAREER_CATALOG:
            if career["name"].lower() in question:
                careers.append(career["name"])

        # Remove duplicates while preserving order
        return list(dict.fromkeys(careers))

    def compare_careers(
        self,
        career_1: str,
        career_2: str,
    ) -> dict | None:
        """
        Compare two careers.
        """

        first = self.get_career(career_1)
        second = self.get_career(career_2)

        if not first or not second:
            return None

        if first["name"] == second["name"]:
            return None

        return {
            "career_1_name": first["name"],
            "career_2_name": second["name"],
            "career_1": first,
            "career_2": second,
        }