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


def seed_careers():
    db: Session = SessionLocal()

    try:
        json_path = PROJECT_ROOT / "datasets" / "careers.json"

        with open(json_path, "r", encoding="utf-8") as file:
            careers = json.load(file)

        inserted = 0

        for career in careers:

            exists = (
                db.query(Career)
                .filter(Career.title == career["title"])
                .first()
            )

            if exists:
                continue

            db.add(Career(**career))
            inserted += 1

        db.commit()

        print(f"✅ Successfully inserted {inserted} career(s).")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_careers()