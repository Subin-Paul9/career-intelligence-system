from app.core.gemini import client
from app.config import settings


def test_connection():
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents="Say hello in one sentence."
    )

    print(response.text)


if __name__ == "__main__":
    test_connection()