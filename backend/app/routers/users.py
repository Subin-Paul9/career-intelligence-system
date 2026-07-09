from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.models.user import User
from app.dependencies.auth_dependencies import get_current_user

router = APIRouter()


# -----------------------------
# Pydantic Schema for Profile Update
# -----------------------------
class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


# -----------------------------
# GET USER PROFILE
# -----------------------------
@router.get(
    "/profile",
    status_code=status.HTTP_200_OK
)
def get_profile(
    current_token: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Returns the authenticated user's profile.
    """

    email = current_token.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "success": True,
        "message": "Profile retrieved successfully",
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    }


# -----------------------------
# UPDATE USER PROFILE
# -----------------------------
@router.put(
    "/profile",
    status_code=status.HTTP_200_OK
)
def update_profile(
    updated_data: UserUpdate,
    current_token: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Updates the authenticated user's profile.
    """

    email = current_token.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if updated_data.first_name is not None:
        user.first_name = updated_data.first_name

    if updated_data.last_name is not None:
        user.last_name = updated_data.last_name

    if updated_data.phone is not None:
        user.phone = updated_data.phone

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "Profile updated successfully"
    }


# -----------------------------
# DELETE (DEACTIVATE) USER
# -----------------------------
@router.delete(
    "/profile",
    status_code=status.HTTP_200_OK
)
def delete_profile(
    current_token: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Deactivates the authenticated user's account.
    """

    email = current_token.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Soft Delete
    user.is_active = False

    db.commit()

    return {
        "success": True,
        "message": "User account deactivated successfully"
    }