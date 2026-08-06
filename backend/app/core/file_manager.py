from pathlib import Path

from app.config.settings import (
    UPLOAD_DIR,
    INTERVIEW_AUDIO_DIR,
    TEMP_AUDIO_DIR,
)


def initialize_upload_directories() -> None:
    """
    Create upload directories if they do not exist.
    """

    directories = [
        UPLOAD_DIR,
        INTERVIEW_AUDIO_DIR,
        TEMP_AUDIO_DIR,
    ]

    for directory in directories:
        Path(directory).mkdir(
            parents=True,
            exist_ok=True,
        )