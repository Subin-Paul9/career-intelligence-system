import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.database.database import SessionLocal
from app.services.career_recommender import recommend_careers


db = SessionLocal()

resume_skills = [
    "Python",
    "SQL",
    "Git",
    "Docker",
    "FastAPI"
]

recommendations = recommend_careers(
    db=db,
    resume_skills=resume_skills,
    top_n=5
)

for career in recommendations:
    print(career)

db.close()