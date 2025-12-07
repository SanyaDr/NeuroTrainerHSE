# app/models/rating.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class RatingEvent(Base):
    __tablename__ = "rating_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    action = Column(String, nullable=False)  # имя из RatingAction
    points = Column(Integer, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User", backref="rating_events")
