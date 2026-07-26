import re

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.resume import Resume
from app.models.recommendation import Recommendation
from app.models.interview_session import InterviewSession
from app.models.skill import Skill


class InterviewContextService:
    """
    Service responsible for building the interview context
    that will be sent to the AI model for generating
    personalized interview questions.
    """

    def __init__(self, db: Session):
        self.db = db

    def build_context(
        self,
        user_id: int,
        difficulty: str,
    ) -> dict:
        """
        Build interview context for AI question generation.
        """

        # --------------------------------------------------
        # Fetch User
        # --------------------------------------------------

        user = (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise ValueError("User not found.")

        # --------------------------------------------------
        # Fetch Latest Resume
        # --------------------------------------------------

        resume = (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.uploaded_at.desc())
            .first()
        )

        if not resume:
            raise ValueError("Resume not found.")

        # --------------------------------------------------
        # Fetch Latest Career Recommendation
        # --------------------------------------------------

        recommendation = (
            self.db.query(Recommendation)
            .filter(Recommendation.user_id == user_id)
            .order_by(Recommendation.generated_at.desc())
            .first()
        )

        if not recommendation:
            raise ValueError("Career recommendation not found.")

        # --------------------------------------------------
        # Extract Candidate Skills from Resume
        # --------------------------------------------------

        resume_text = (
            resume.resume_text or ""
        ).lower().replace("-", " ")

        all_skills = (
            self.db.query(Skill)
            .order_by(Skill.name)
            .all()
        )

        candidate_skills = []

        for skill in all_skills:

            skill_name = skill.name.lower().replace("-", " ")

            # -----------------------------
            # Handle ambiguous skills
            # -----------------------------

            if skill_name == "java":
                pattern = r"\bjava\b(?!script)"

            elif skill_name == "c":
                pattern = r"\bc\b"

            elif skill_name == "c++":
                pattern = r"\bc\+\+"

            elif skill_name == "go":
                pattern = r"\bgo(lang)?\b"

            elif skill_name == "sql":
                pattern = r"\bsql\b"

            else:
                pattern = r"\b" + re.escape(skill_name) + r"\b"

            if re.search(pattern, resume_text):
                candidate_skills.append(skill.name)

        # Remove duplicates and sort alphabetically
        candidate_skills = sorted(set(candidate_skills))

        # --------------------------------------------------
        # Calculate Previous Interview Score
        # --------------------------------------------------

        previous_sessions = (
            self.db.query(InterviewSession)
            .filter(InterviewSession.user_id == user_id)
            .filter(InterviewSession.overall_score.isnot(None))
            .all()
        )

        previous_interview_score = None

        if previous_sessions:

            total_score = sum(
                session.overall_score
                for session in previous_sessions
            )

            previous_interview_score = round(
                total_score / len(previous_sessions),
                2
            )

        # --------------------------------------------------
        # Build Interview Context
        # --------------------------------------------------

        context = {
            "user_id": user.id,
            "difficulty": difficulty,

            # Resume Information
            "resume_text": resume.resume_text,
            "ats_score": resume.ats_score,
            "resume_feedback": resume.feedback,

            # Extracted Skills
            "skills": candidate_skills,

            # Career Recommendation
            "career": recommendation.career,
            "match_score": recommendation.match_score,

            # Missing Skills
            "missing_skills": (
                [
                    skill.strip()
                    for skill in recommendation.missing_skills.split(",")
                ]
                if recommendation.missing_skills
                else []
            ),

            # Previous Interview Performance
            "previous_interview_score": previous_interview_score,
        }

        return context