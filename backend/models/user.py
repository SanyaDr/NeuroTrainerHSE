from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Float
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    fitness_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    preferences = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

