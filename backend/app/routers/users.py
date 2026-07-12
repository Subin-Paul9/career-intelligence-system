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
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Returns the authenticated user's profile.
    """

    return {
        "success": True,
        "message": "Profile retrieved successfully",
        "user": {
            "id": current_user.id,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email,
            "phone": current_user.phone,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Updates the authenticated user's profile.
    """

    if updated_data.first_name is not None:
        current_user.first_name = updated_data.first_name

    if updated_data.last_name is not None:
        current_user.last_name = updated_data.last_name

    if updated_data.phone is not None:
        current_user.phone = updated_data.phone

    db.commit()
    db.refresh(current_user)

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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Deactivates the authenticated user's account.
    """

    current_user.is_active = False

    db.commit()

    return {
        "success": True,
        "message": "User account deactivated successfully"
    }