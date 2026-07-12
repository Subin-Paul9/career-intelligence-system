
import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.models.resume import Resume
from app.models.user import User

from app.schemas.resume import (
    ResumeResponse,
    ResumeHistoryResponse,
    ResumeDetailsResponse,
)

from app.utils.resume_parser import extract_text
from app.utils.ats_analyzer import calculate_ats_score
from app.utils.suggestion_generator import generate_suggestions

router = APIRouter()

UPLOAD_DIR = "uploads"

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

# Maximum file size (5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

os.makedirs(UPLOAD_DIR, exist_ok=True)


# =====================================================
# Upload Resume
# =====================================================
@router.post(
    "/upload",
    response_model=ResumeResponse,
    summary="Upload Resume"
)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a resume file.

    - Accepts only PDF and DOCX files.
    - Maximum allowed size: 5 MB.
    """

    # Validate file extension
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    # Validate file size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must not exceed 5 MB."
        )

    # Generate unique filename
    unique_filename = f"{uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save metadata
    resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_path,
        ats_score=None,
        resume_text=None
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


# =====================================================
# Parse Resume
# =====================================================
@router.get(
    "/parse/{resume_id}",
    summary="Extract Resume Text"
)
def parse_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Extract text from an uploaded resume and store it in the database.
    """

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    # Check if the uploaded file still exists
    if not os.path.exists(resume.file_path):
        raise HTTPException(
            status_code=404,
            detail="Resume file not found on server."
        )

    # Extract text from the resume
    extracted_text = extract_text(resume.file_path)

    # Save extracted text in the database
    resume.resume_text = extracted_text

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "text": resume.resume_text
    }

@router.get(
    "/ats/{resume_id}",
    summary="Calculate ATS Score"
)
def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Calculate a basic ATS score for a parsed resume.
    """

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    if not resume.resume_text:
        raise HTTPException(
            status_code=400,
            detail="Please parse the resume before calculating the ATS score."
        )

    result = calculate_ats_score(resume.resume_text)

    # Save ATS score
    resume.ats_score = result["ats_score"]

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "ats_score": resume.ats_score,
        "breakdown": result["breakdown"]
    }

@router.get(
    "/suggestions/{resume_id}",
    summary="Generate Resume Suggestions"
)
def resume_suggestions(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate improvement suggestions for a resume.
    """

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    if not resume.resume_text:
        raise HTTPException(
            status_code=400,
            detail="Please parse the resume first."
        )

    suggestions = generate_suggestions(resume.resume_text)

    # Save feedback to the database
    resume.feedback = "\n".join(suggestions)

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "ats_score": resume.ats_score,
        "suggestions": suggestions
    }

@router.get(
    "/history",
    response_model=list[ResumeHistoryResponse],
    summary="Resume History"
)
def get_resume_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.uploaded_at.desc())
        .all()
    )

    return resumes

# =====================================================
# Resume Details
# =====================================================
@router.get(
    "/{resume_id}",
    response_model=ResumeDetailsResponse,
    summary="Resume Details"
)
def get_resume_details(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns complete information about a specific resume.
    """

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    return resume

# =====================================================
# Delete Resume
# =====================================================
@router.delete(
    "/{resume_id}",
    summary="Delete Resume"
)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a resume and its uploaded file.
    """

    # Find the resume belonging to the logged-in user
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    # Delete the uploaded file if it exists
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    # Delete the database record
    db.delete(resume)
    db.commit()

    return {
        "success": True,
        "message": "Resume deleted successfully."
    }