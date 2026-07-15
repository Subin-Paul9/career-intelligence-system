from sqlalchemy import Column, Integer, ForeignKey

from app.database.base import Base


class CareerSkill(Base):
    __tablename__ = "career_skills"

    career_id = Column(
        Integer,
        ForeignKey("careers.id", ondelete="CASCADE"),
        primary_key=True
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True
    )