import re


def calculate_ats_score(text: str) -> dict:
    """
    Basic ATS scoring based on common resume sections.
    """

    text = text.lower()

    score = 0

    breakdown = {}

    # -----------------------------
    # Contact (10)
    # -----------------------------
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone = re.search(r"\b\d{10}\b", text)

    contact = 10 if (email and phone) else 5 if (email or phone) else 0

    breakdown["contact"] = contact
    score += contact

    # -----------------------------
    # Skills (20)
    # -----------------------------
    skills = [
        "python",
        "java",
        "c++",
        "sql",
        "html",
        "css",
        "javascript",
        "react",
        "fastapi",
        "django",
        "flask",
        "git",
        "docker",
        "aws",
        "mongodb"
    ]

    found = sum(1 for skill in skills if skill in text)

    skills_score = min(20, found * 2)

    breakdown["skills"] = skills_score
    score += skills_score

    # -----------------------------
    # Education (20)
    # -----------------------------
    education_keywords = [
        "b.tech",
        "btech",
        "b.e",
        "be",
        "bachelor",
        "bachelor of engineering",
        "bachelor of technology",
        "master",
        "m.tech",
        "mtech",
        "m.e",
        "degree",
        "university",
        "college",
        "engineering",
        "computer science",
        "cgpa",
        "gpa"
    ]

    education = (
        20
        if any(keyword in text for keyword in education_keywords)
        else 0
    )

    breakdown["education"] = education
    score += education

    # -----------------------------
    # Experience (30)
    # -----------------------------
    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "worked",
        "software engineer",
        "developer"
    ]

    experience = (
        30
        if any(keyword in text for keyword in experience_keywords)
        else 0
    )

    breakdown["experience"] = experience
    score += experience

    # -----------------------------
    # Projects (20)
    # -----------------------------
    project_keywords = [
        "project",
        "projects",
        "github",
        "portfolio"
    ]

    projects = (
        20
        if any(keyword in text for keyword in project_keywords)
        else 0
    )

    breakdown["projects"] = projects
    score += projects

    return {
        "ats_score": score,
        "breakdown": breakdown
    }