import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.database.database import SessionLocal
from app.utils.skill_matcher import match_skills


db = SessionLocal()

resume_skills = [
    "Python",
    "Git"
]

result = match_skills(
    db=db,
    career_title="Software Engineer",
    resume_skills=resume_skills
)

print(result)

db.close()