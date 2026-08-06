import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config.settings import (
    INTERVIEW_AUDIO_DIR,
    MAX_AUDIO_FILE_SIZE,
)
from app.models.interview_answer import InterviewAnswer
from app.models.interview_audio import InterviewAudio
from app.models.user import User
from app.schemas.voice_interview import (
    VoiceUploadResponse,
)


class AudioUploadService:
    """
    Service responsible for:

    - Validating uploaded audio files
    - Saving recordings
    - Creating upload directories
    - Storing metadata
    """

    ALLOWED_EXTENSIONS = {
        ".wav",
        ".mp3",
        ".m4a",
        ".webm",
    }

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Audio Validation
    # =====================================================

    async def validate_audio(
        self,
        file: UploadFile,
    ) -> None:
        """
        Validate uploaded audio file.
        """

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No audio file provided.",
            )

        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported audio format. "
                    "Allowed formats: wav, mp3, m4a, webm."
                ),
            )

        content = await file.read()

        if len(content) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded audio file is empty.",
            )

        if len(content) > MAX_AUDIO_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Audio file exceeds the maximum size of 25 MB.",
            )

        # Reset file pointer after validation
        await file.seek(0)

    # =====================================================
    # Filename Generation
    # =====================================================

    def generate_filename(
        self,
        answer_id: int,
        original_filename: str,
    ) -> str:
        """
        Generate a unique filename for the uploaded audio.
        """

        extension = Path(
            original_filename
        ).suffix.lower()

        unique_id = uuid.uuid4().hex

        return (
            f"answer_{answer_id}_{unique_id}"
            f"{extension}"
        )

    # =====================================================
    # Upload Directory
    # =====================================================

    def create_upload_directory(
        self,
        user_id: int,
        session_id: int,
    ) -> Path:
        """
        Create the upload directory for a user's
        interview session.

        uploads/
            interview_audio/
                user_<id>/
                    session_<id>/
        """

        upload_directory = (
            Path(INTERVIEW_AUDIO_DIR)
            / f"user_{user_id}"
            / f"session_{session_id}"
        )

        upload_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return upload_directory

    # =====================================================
    # Save Audio File
    # =====================================================

    async def save_audio(
        self,
        file: UploadFile,
        upload_directory: Path,
        filename: str,
    ) -> tuple[str, int]:
        """
        Save the uploaded audio file.

        Returns:
            (file_path, file_size)
        """

        file_path = upload_directory / filename

        content = await file.read()

        with open(
            file_path,
            "wb",
        ) as audio_file:
            audio_file.write(content)

        # Reset file pointer
        await file.seek(0)

        return (
            str(file_path),
            len(content),
        )

    # =====================================================
    # Database Record
    # =====================================================

    def create_audio_record(
        self,
        answer_id: int,
        file_name: str,
        file_path: str,
        file_size: int,
        audio_format: str,
    ) -> InterviewAudio:
        """
        Create a database record for the uploaded audio.
        """

        audio = InterviewAudio(
            answer_id=answer_id,
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            duration=None,
            audio_format=audio_format,
        )

        try:
            self.db.add(audio)
            self.db.commit()
            self.db.refresh(audio)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Failed to store audio metadata.",
            ) from e

        return audio

    # =====================================================
    # Upload Audio
    # =====================================================

    async def upload_audio(
        self,
        answer_id: int,
        file: UploadFile,
        user: User,
    ) -> VoiceUploadResponse:
        """
        Upload an interview audio recording.
        """

        # -------------------------------------------------
        # Validate Interview Answer
        # -------------------------------------------------

        answer = (
            self.db.query(InterviewAnswer)
            .filter(
                InterviewAnswer.id == answer_id
            )
            .first()
        )

        if answer is None:
            raise HTTPException(
                status_code=404,
                detail="Interview answer not found.",
            )

        # -------------------------------------------------
        # Get Interview Context
        # -------------------------------------------------

        question = answer.question
        if question is None:
            raise HTTPException(
                status_code=404,
                detail="Interview question not found.",
            )
            
        session = question.session
        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Interview session not found.",
            )

        user_id = session.user_id
        session_id = session.id

        # -------------------------------------------------
        # Verify Ownership
        # -------------------------------------------------

        if session.user_id != user.id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You are not authorized to upload "
                    "audio for this interview."
                ),
            )

        # -------------------------------------------------
        # Check Existing Audio
        # -------------------------------------------------

        existing_audio = (
            self.db.query(InterviewAudio)
            .filter(
                InterviewAudio.answer_id == answer_id
            )
            .first()
        )

        if existing_audio:
            raise HTTPException(
                status_code=400,
                detail="Audio has already been uploaded for this interview answer.",
            )

        # -------------------------------------------------
        # Validate Audio
        # -------------------------------------------------

        await self.validate_audio(file)

        # -------------------------------------------------
        # Generate Filename
        # -------------------------------------------------

        filename = self.generate_filename(
            answer_id=answer_id,
            original_filename=file.filename,
        )

        # -------------------------------------------------
        # Create Upload Directory
        # -------------------------------------------------

        upload_directory = self.create_upload_directory(
            user_id=user_id,
            session_id=session_id,
        )

        # -------------------------------------------------
        # Save Audio
        # -------------------------------------------------

        file_path, file_size = await self.save_audio(
            file=file,
            upload_directory=upload_directory,
            filename=filename,
        )

        # -------------------------------------------------
        # Store Metadata
        # -------------------------------------------------

        audio = self.create_audio_record(
            answer_id=answer_id,
            file_name=filename,
            file_path=file_path,
            file_size=file_size,
            audio_format=Path(filename).suffix.lower(),
        )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return VoiceUploadResponse(
            audio_id=audio.id,
            answer_id=audio.answer_id,
            file_name=audio.file_name,
            file_size=audio.file_size,
            duration=audio.duration,
            audio_format=audio.audio_format,
            message="Audio uploaded successfully.",
        )