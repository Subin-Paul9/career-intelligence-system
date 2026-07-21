from google import genai

from app.config import settings


def get_gemini_client() -> genai.Client:
    """
    Create and return a reusable Gemini client.
    """

    if not settings.GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not configured in backend/.env"
        )

    return genai.Client(
        api_key=settings.GEMINI_API_KEY
    )


# Singleton Gemini client
client = get_gemini_client()


def generate_content(prompt: str):
    """
    Generate content using the configured Gemini model.
    """

    return client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )