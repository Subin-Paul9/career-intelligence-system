import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.database.database import SessionLocal
from app.services.career_summary_service import (
    generate_career_summary
)

db = SessionLocal()

resume_skills = [
    "Python",
    "SQL",
    "Git"
]

result = generate_career_summary(
    db=db,
    resume_skills=resume_skills
)

from pprint import pprint
pprint(result)

db.close()