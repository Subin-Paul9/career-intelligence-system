from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# =====================================================
# Base Schema
# =====================================================
class ResumeBase(BaseModel):
    file_name: str


# =====================================================
# Create Schema
# =====================================================
class ResumeCreate(ResumeBase):
    pass


# =====================================================
# Upload Response Schema
# =====================================================
class ResumeResponse(ResumeBase):
    id: int
    user_id: int
    file_path: str
    ats_score: Optional[int] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Resume History Response Schema
# =====================================================
class ResumeHistoryResponse(BaseModel):
    id: int
    file_name: str
    ats_score: Optional[int] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True

# =====================================================
# Resume Details Response Schema
# =====================================================
class ResumeDetailsResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    ats_score: Optional[int] = None
    resume_text: Optional[str] = None
    feedback: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True        