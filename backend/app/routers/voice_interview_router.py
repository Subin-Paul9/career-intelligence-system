from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth_dependencies import (
    get_current_user,
)
from app.models.user import User

from app.schemas.voice_interview import (
    VoiceUploadResponse,
    TranscriptResponse,
)

from app.schemas.voice_report import (
    VoiceInterviewReportResponse,
)

from app.schemas.voice_history import (
    VoiceHistoryResponse,
)

from app.services.audio_upload_service import (
    AudioUploadService,
)

from app.services.speech_to_text_service import (
    SpeechToTextService,
)

from app.services.voice_interview_service import (
    VoiceInterviewService,
)

from app.services.voice_report_service import (
    VoiceReportService,
)

from app.services.voice_history_service import (
    VoiceHistoryService,
)


router = APIRouter(
    prefix="/api/interview",
    tags=["Voice Interview"],
)


# =====================================================
# Upload Interview Audio
# =====================================================

@router.post(
    "/upload-audio",
    response_model=VoiceUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_audio(
    answer_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload an interview audio recording.
    """

    service = AudioUploadService(
        db=db,
    )

    return await service.upload_audio(
        answer_id=answer_id,
        file=file,
        user=current_user,
    )


# =====================================================
# Generate Transcript
# =====================================================

@router.post(
    "/transcribe",
    response_model=TranscriptResponse,
    status_code=status.HTTP_200_OK,
)
def generate_transcript(
    audio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a transcript from an uploaded
    interview audio recording.
    """

    service = SpeechToTextService(
        db=db,
    )

    return service.generate_transcript(
        audio_id=audio_id,
    )


# =====================================================
# Analyze Voice Interview
# =====================================================

@router.post(
    "/analyze",
    response_model=VoiceInterviewReportResponse,
    status_code=status.HTTP_200_OK,
)
def analyze_voice_interview(
    audio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Execute the complete voice interview
    analysis pipeline and return the
    final interview report.
    """

    service = VoiceInterviewService(
        db=db,
    )

    return service.analyze(
        user=current_user,
        audio_id=audio_id,
    )


# =====================================================
# Get Transcript
# =====================================================

@router.get(
    "/transcript/{audio_id}",
    response_model=TranscriptResponse,
    status_code=status.HTTP_200_OK,
)
def get_transcript(
    audio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve an existing transcript
    for an interview audio recording.
    """

    service = SpeechToTextService(
        db=db,
    )

    return service.get_transcript(
        audio_id=audio_id,
    )


# =====================================================
# Get Voice Interview Report
# =====================================================

@router.get(
    "/report/{session_id}",
    response_model=VoiceInterviewReportResponse,
    status_code=status.HTTP_200_OK,
)
def get_voice_report(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the saved voice interview report
    for an interview session.
    """

    service = VoiceReportService(
        db=db,
    )

    return service.get_report_by_session(
        session_id=session_id,
    )


# =====================================================
# Voice Interview History
# =====================================================

@router.get(
    "/voice-history",
    response_model=VoiceHistoryResponse,
    status_code=status.HTTP_200_OK,
)
def get_voice_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the voice interview history
    for the currently authenticated user.
    """

    service = VoiceHistoryService(
        db=db,
    )

    return service.get_history(
        user=current_user,
    )