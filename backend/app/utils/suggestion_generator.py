def generate_suggestions(text: str) -> list[str]:
    """
    Generate resume improvement suggestions based on
    missing sections and keywords.
    """

    text = text.lower()

    suggestions = []

    # Technical skills
    technical_skills = [
        "python",
        "java",
        "c++",
        "sql",
        "javascript",
        "react",
        "fastapi",
        "django",
        "docker",
        "aws"
    ]

    found_skills = sum(skill in text for skill in technical_skills)

    if found_skills < 5:
        suggestions.append("Add more technical skills.")

    # Certifications
    certification_keywords = [
        "certification",
        "certificate",
        "aws certified",
        "coursera",
        "udemy",
        "nptel"
    ]

    if not any(word in text for word in certification_keywords):
        suggestions.append("Include certifications.")

    # Internship
    internship_keywords = [
        "internship",
        "intern"
    ]

    if not any(word in text for word in internship_keywords):
        suggestions.append("Mention internships.")

    # Projects
    if "project" not in text:
        suggestions.append("Add project descriptions.")

    # Achievements
    achievement_keywords = [
        "achieved",
        "improved",
        "increased",
        "reduced",
        "%",
        "developed",
        "implemented"
    ]

    if not any(word in text for word in achievement_keywords):
        suggestions.append("Add measurable achievements.")

    # Default
    if not suggestions:
        suggestions.append("Excellent resume! No major improvements detected.")

    return suggestions