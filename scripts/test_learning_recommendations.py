import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.database.database import SessionLocal
from app.services.learning_recommendation_service import (
    recommend_learning_resources
)

db = SessionLocal()

resume_skills = [
    "Python",
    "SQL",
    "Git"
]

recommendations = recommend_learning_resources(
    db=db,
    career_title="Software Engineer",
    resume_skills=resume_skills
)

for item in recommendations:
    print(item)

db.close()