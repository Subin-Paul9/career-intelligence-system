from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import UserRegister, UserLogin
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """
    USER REGISTRATION ENDPOINT
    Validates the input payload, hashes the password securely,
    and writes the record directly to the PostgreSQL users table.
    """

    # Check if the email already exists
    user_exists = db.query(User).filter(User.email == user_in.email).first()

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_pwd = hash_password(user_in.password)

    # Create new user
    new_user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        password=hashed_pwd,
        phone=user_in.phone,
        role="student"
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


@router.post("/login")
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db)
) -> dict:
    """
    Authenticates a user and returns a JWT access token.
    """

    # Check whether the email exists
    user = db.query(User).filter(
        User.email == user_in.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(
        user_in.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT
    access_token = create_access_token(
        data={
            "id": user.id,
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }