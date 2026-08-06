from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession
from app.models.user import User

from app.schemas.voice_history import (
    VoiceHistoryItemResponse,
    VoiceHistoryResponse,
)


class VoiceHistoryService:
    """
    Service responsible for:

    - Loading user's voice interview history
    - Returning completed voice interviews
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Load Voice Interview Sessions
    # =====================================================

    def load_sessions(
        self,
        user: User,
    ) -> list[InterviewSession]:
        """
        Load all voice interview sessions
        belonging to the current user.
        """

        return (
            self.db.query(
                InterviewSession,
            )
            .filter(
                InterviewSession.user_id == user.id,
                InterviewSession.interview_type == "VOICE",
            )
            .order_by(
                InterviewSession.created_at.desc(),
            )
            .all()
        )

    # =====================================================
    # Build History Item
    # =====================================================

    def build_history_item(
        self,
        session: InterviewSession,
    ) -> VoiceHistoryItemResponse:
        """
        Convert an InterviewSession
        into a response object.
        """

        return VoiceHistoryItemResponse(
            session_id=session.id,
            interview_type=session.interview_type,
            difficulty=session.difficulty,
            answered_questions=session.answered_questions,
            total_questions=session.total_questions,
            overall_score=session.overall_score,
            completed_at=session.completed_at,
        )

    # =====================================================
    # Get Voice Interview History
    # =====================================================

    def get_history(
        self,
        user: User,
    ) -> VoiceHistoryResponse:
        """
        Return all voice interview
        sessions for the current user.
        """

        sessions = self.load_sessions(
            user=user,
        )

        history = [
            self.build_history_item(
                session,
            )
            for session in sessions
        ]

        return VoiceHistoryResponse(
            history=history,
        )