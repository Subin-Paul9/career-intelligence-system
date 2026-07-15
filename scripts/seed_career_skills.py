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
from app.models.career import Career
from app.models.skill import Skill
from app.models.career_skill import CareerSkill


def seed_career_skills():
    db: Session = SessionLocal()

    try:
        json_path = PROJECT_ROOT / "datasets" / "career_skills.json"

        with open(json_path, "r", encoding="utf-8") as file:
            mappings = json.load(file)

        inserted = 0

        for career_title, skill_names in mappings.items():

            career = (
                db.query(Career)
                .filter(Career.title == career_title)
                .first()
            )

            if not career:
                print(f"❌ Career not found: {career_title}")
                continue

            for skill_name in skill_names:

                skill = (
                    db.query(Skill)
                    .filter(Skill.name == skill_name)
                    .first()
                )

                if not skill:
                    print(f"❌ Skill not found: {skill_name}")
                    continue

                exists = (
                    db.query(CareerSkill)
                    .filter(
                        CareerSkill.career_id == career.id,
                        CareerSkill.skill_id == skill.id
                    )
                    .first()
                )

                if exists:
                    continue

                db.add(
                    CareerSkill(
                        career_id=career.id,
                        skill_id=skill.id
                    )
                )

                inserted += 1

        db.commit()

        print(f"✅ Successfully inserted {inserted} career-skill mappings.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_career_skills()