from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.auth import verify_access_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Extracts and validates the JWT access token.
    """

    token = credentials.credentials

    payload = verify_access_token(token)

    return payload