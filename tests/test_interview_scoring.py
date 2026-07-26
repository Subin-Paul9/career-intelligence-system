import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "backend",
        )
    ),
)

from app.services.interview_scoring import InterviewScoringService


def main():
    service = InterviewScoringService()

    evaluation = {
        "technical_score": 90,
        "practical_score": 80,
        "explanation_quality": 85,
        "communication_score": 85,
        "missing_concepts": [
            "Docker networking"
        ],
    }

    result = service.calculate_score(evaluation)

    print(result)


if __name__ == "__main__":
    main()