from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
)

from sqlalchemy.sql import func

from app.database.base import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, nullable=False)

    resume_id = Column(Integer, nullable=False)

    career = Column(String, nullable=False)

    match_score = Column(Float, nullable=False)

    # Store as comma-separated text
    missing_skills = Column(String, nullable=True)

    generated_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False,
)