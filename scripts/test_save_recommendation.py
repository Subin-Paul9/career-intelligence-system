from app.database.database import SessionLocal

from app.services.career_summary_service import generate_career_summary
from app.services.recommendation_service import save_recommendation


def main():
    db = SessionLocal()

    try:
        # Generate a career summary from sample resume skills
        summary = generate_career_summary(
            db=db,
            resume_skills=[
                "Python",
                "Git",
                "SQL",
            ]
        )

        # Save the recommendation
        recommendation = save_recommendation(
            db=db,
            user_id=1,
            resume_id=1,
            summary=summary,
        )

        print("Recommendation saved successfully!")
        print(f"ID: {recommendation.id}")
        print(f"Career: {recommendation.career}")
        print(f"Match Score: {recommendation.match_score}")
        print(f"Missing Skills: {recommendation.missing_skills}")

    finally:
        db.close()


if __name__ == "__main__":
    main()