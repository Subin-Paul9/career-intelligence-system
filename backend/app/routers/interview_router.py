from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.core.rate_limiter import limiter

from app.models.user import User

from app.schemas.interview import (
    InterviewStartRequest,
    InterviewStartResponse,
    RetryInterviewResponse,
    InterviewAnswerRequest,
    InterviewHistoryResponse,
    InterviewDetailResponse,
    DeleteInterviewResponse,
)

from app.services.interview_service import InterviewService


router = APIRouter(
    prefix="/api/interview",
    tags=["AI Mock Interview"],
)


# =====================================================
# Start Interview
# =====================================================

@router.post(
    "/start",
    response_model=InterviewStartResponse,
    summary="Start AI Mock Interview",
)
@limiter.limit("5/minute")
def start_interview(
    request: Request,
    data: InterviewStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Start a new AI mock interview.
    """

    service = InterviewService(db)

    result = service.start_interview(
        user=current_user,
        data=data,
    )

    return InterviewStartResponse(
        session_id=result["session_id"],
        question=result["questions"][0]["question"],
    )


# =====================================================
# Retry Interview
# =====================================================

@router.post(
    "/{session_id}/retry",
    response_model=RetryInterviewResponse,
    summary="Retry AI Mock Interview",
)
@limiter.limit("5/minute")
def retry_interview(
    request: Request,
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retry a previous AI mock interview.
    Creates a new interview session while
    preserving the original interview.
    """

    service = InterviewService(db)

    result = service.retry_interview(
        session_id=session_id,
        user=current_user,
    )

    return RetryInterviewResponse(
        session_id=result["session_id"],
        attempt_number=result["attempt_number"],
        question=result["questions"][0]["question"],
    )


# =====================================================
# Get Next Question
# =====================================================

@router.get(
    "/{session_id}/question",
    summary="Get Next Interview Question",
)
def next_question(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the next interview question.
    """

    service = InterviewService(db)

    return service.get_next_question(session_id)


# =====================================================
# Submit Answer
# =====================================================

@router.post(
    "/{session_id}/answer",
    summary="Submit Interview Answer",
)
@limiter.limit("10/minute")
def submit_answer(
    request: Request,
    session_id: int,
    data: InterviewAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit an answer for evaluation.
    """

    service = InterviewService(db)

    return service.submit_answer(
        session_id,
        data,
    )


# =====================================================
# Finish Interview
# =====================================================

@router.post(
    "/{session_id}/finish",
    summary="Finish Interview",
)
@limiter.limit("5/minute")
def finish_interview(
    request: Request,
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Finish interview and generate report.
    """

    service = InterviewService(db)

    return service.finish_interview(session_id)


# =====================================================
# Interview History
# =====================================================

@router.get(
    "/history",
    response_model=list[InterviewHistoryResponse],
    summary="Interview History",
)
def interview_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return interview history for the logged-in user.
    """

    service = InterviewService(db)

    return service.get_history(current_user)


# =====================================================
# Interview Details
# =====================================================

@router.get(
    "/{session_id}",
    response_model=InterviewDetailResponse,
    summary="Interview Details",
)
def interview_details(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return complete interview details.
    """

    service = InterviewService(db)

    return service.get_interview_details(
        session_id=session_id,
        user=current_user,
    )


# =====================================================
# Delete Interview
# =====================================================

@router.delete(
    "/{session_id}",
    response_model=DeleteInterviewResponse,
    summary="Delete Interview",
)
def delete_interview(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete an interview session belonging to the logged-in user.
    """

    service = InterviewService(db)

    return service.delete_interview(
        session_id=session_id,
        user=current_user,
    )