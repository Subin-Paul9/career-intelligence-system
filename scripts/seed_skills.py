import json
import sys
from pathlib import Path

from sqlalchemy.orm import Session

# -------------------------------------------------
# Add backend directory to Python path
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

# -------------------------------------------------
# Import application modules
# -------------------------------------------------
from app.database.database import SessionLocal
from app.models.skill import Skill


def seed_skills():
    db: Session = SessionLocal()

    try:
        json_path = PROJECT_ROOT / "datasets" / "skills.json"

        with open(json_path, "r", encoding="utf-8") as file:
            skills_data = json.load(file)

        inserted = 0

        # Loop through every category
        for _, skills in skills_data.items():

            for skill_name in skills:

                exists = (
                    db.query(Skill)
                    .filter(Skill.name == skill_name)
                    .first()
                )

                if exists:
                    continue

                db.add(Skill(name=skill_name))
                inserted += 1

        db.commit()

        print(f"✅ Successfully inserted {inserted} skills.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_skills()