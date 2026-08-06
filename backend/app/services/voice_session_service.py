from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession
from app.models.user import User


class VoiceSessionService:
    """
    Service responsible for managing
    Voice Interview sessions.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Create Voice Interview Session
    # =====================================================

    def create_session(
        self,
        user: User,
        difficulty: str = "Medium",
    ) -> InterviewSession:
        """
        Create a new voice interview session.
        """

        session = InterviewSession(
            user_id=user.id,
            interview_type="VOICE",
            difficulty=difficulty,
            status="ACTIVE",
            total_questions=1,
            answered_questions=0,
            attempt_number=1,
        )

        self.db.add(session)

        try:

            self.db.commit()

            self.db.refresh(session)

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to create voice interview session.",
            ) from e

        return session

    # =====================================================
    # Complete Voice Interview Session
    # =====================================================

    def complete_session(
        self,
        session: InterviewSession,
        overall_score: float,
    ) -> InterviewSession:
        """
        Mark a voice interview session as completed
        and store the final score.
        """

        session.status = "COMPLETED"

        session.answered_questions = (
            session.total_questions
        )

        session.overall_score = overall_score

        session.completed_at = datetime.now(
            timezone.utc,
        )

        try:

            self.db.commit()

            self.db.refresh(
                session,
            )

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to complete voice interview session.",
            ) from e

        return session

    # =====================================================
    # Get Voice Interview Session
    # =====================================================

    def get_session(
        self,
        session_id: int,
    ) -> InterviewSession:
        """
        Retrieve a voice interview session.
        """

        session = (
            self.db.query(
                InterviewSession,
            )
            .filter(
                InterviewSession.id == session_id,
                InterviewSession.interview_type == "VOICE",
            )
            .first()
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Voice interview session not found.",
            )

        return session