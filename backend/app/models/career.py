from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.base import Base


class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False, unique=True)

    description = Column(Text, nullable=False)

    average_salary = Column(String(50), nullable=True)

    experience_level = Column(String(50), nullable=False)

    # Optional: relationship for future modules
    # recommendations = relationship(
    #     "Recommendation",
    #     back_populates="career"
    # )