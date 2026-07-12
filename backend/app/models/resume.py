from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    file_name = Column(String(255), nullable=False)

    file_path = Column(String(500), nullable=False)

    # Stores the extracted text from the uploaded resume
    resume_text = Column(Text, nullable=True)

    # ATS score
    ats_score = Column(Integer, nullable=True)

    # Stores generated feedback/suggestions
    feedback = Column(Text, nullable=True)

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationship with User
    user = relationship("User", back_populates="resumes")