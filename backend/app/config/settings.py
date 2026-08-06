import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME")
APP_VERSION = os.getenv("APP_VERSION")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT", 8000))

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

# ===============================
# Gemini Configuration
# ===============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash"
)

GEMINI_TEMPERATURE = float(
    os.getenv("GEMINI_TEMPERATURE", 0.3)
)

GEMINI_MAX_OUTPUT_TOKENS = int(
    os.getenv("GEMINI_MAX_OUTPUT_TOKENS", 2048)
)

# ===============================
# Whisper Configuration
# ===============================

WHISPER_MODEL = os.getenv(
    "WHISPER_MODEL",
    "base"
)

# ===============================
# Upload Configuration
# ===============================

UPLOAD_DIR = os.getenv(
    "UPLOAD_DIR",
    "uploads"
)

INTERVIEW_AUDIO_DIR = os.getenv(
    "INTERVIEW_AUDIO_DIR",
    "uploads/interview_audio"
)

TEMP_AUDIO_DIR = os.getenv(
    "TEMP_AUDIO_DIR",
    "uploads/temp"
)

# ===============================
# Audio Upload Configuration
# ===============================

MAX_AUDIO_FILE_SIZE = int(
    os.getenv(
        "MAX_AUDIO_FILE_SIZE",
        25 * 1024 * 1024,  # 25 MB
    )
)