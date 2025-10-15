from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)

    user_progress = relationship("UserProgress", back_populates="user", uselist=False, cascade="all, delete-orphan")
    speech_recordings = relationship("SpeechRecording", back_populates="user", cascade="all, delete-orphan")


class UserProgress(BaseModel):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_recordings = Column(Integer, default=0)
    average_score = Column(DECIMAL(5, 2))
    last_recording_date = Column(DateTime)

    user = relationship("User", back_populates="user_progress")

