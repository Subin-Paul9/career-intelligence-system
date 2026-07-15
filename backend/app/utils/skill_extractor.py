import json
import re
from pathlib import Path

# --------------------------------------------------
# Load skills dataset
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]

SKILLS_PATH = PROJECT_ROOT / "datasets" / "skills.json"

with open(SKILLS_PATH, "r", encoding="utf-8") as file:
    SKILLS = json.load(file)


# --------------------------------------------------
# Extract skills from resume text
# --------------------------------------------------
def extract_skills(resume_text: str) -> dict:
    """
    Extract skills from resume text based on the predefined skills dataset.
    Returns a dictionary categorized by skill type.
    """

    text = resume_text.lower()

    extracted = {
        "programming_languages": [],
        "frameworks": [],
        "databases": [],
        "tools": [],
        "soft_skills": [],
        "certifications": []
    }

    for category, skill_list in SKILLS.items():

        for skill in skill_list:

            # Match complete words/phrases only
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, text):
                extracted[category].append(skill)

    return extracted