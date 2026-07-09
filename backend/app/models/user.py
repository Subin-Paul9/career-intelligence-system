from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from datetime import datetime

from app.database.base import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(100))

    last_name = Column(String(100))

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    phone = Column(String(20))

    role = Column(
        String(20),
        default="student"
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )