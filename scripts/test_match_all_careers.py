import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.database.database import SessionLocal
from app.utils.skill_matcher import match_all_careers

db = SessionLocal()

resume_skills = [
    "Python",
    "Git",
    "Docker",
    "FastAPI",
    "SQL"
]

results = match_all_careers(
    db=db,
    resume_skills=resume_skills
)

for result in results:
    print(result)

db.close()