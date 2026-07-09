from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import JWTError, jwt

# Ensure this matches your actual configuration directory structure
from app.config.settings import SECRET_KEY

ALGORITHM = "HS256"


def create_access_token(data: dict) -> str:
    """
    Generates a cryptographically signed JWT access token.
    Appends a timezone-aware expiration timestamp set to 1 hour from issuance.
    """
    payload = data.copy()

    # Fixed deprecation: Using modern timezone-aware UTC datetime
    expire = datetime.now(timezone.utc) + timedelta(hours=1)

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_access_token(token: str) -> dict:
    """
    Verifies and decodes an incoming JWT access token.
    Returns the payload if valid; raises an HTTP 401 Unauthorized exception if not.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )