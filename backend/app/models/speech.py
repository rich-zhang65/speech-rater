from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Enum
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.speech import SpeechGradeImprovementCategory

class SpeechRecording(BaseModel):
    __tablename__ = "speech_recordings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    transcription = Column(Text, nullable=False)
    s3_key = Column(String(512))
    duration_seconds = Column(DECIMAL(10, 2))
    word_count = Column(Integer)
    
    user = relationship('User', back_populates='speech_recordings')
    speech_grade = relationship('SpeechGrade', back_populates='recording', uselist=False, cascade='all, delete-orphan')


class SpeechGrade(BaseModel):
    __tablename__ = "speech_grades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recording_id = Column(Integer, ForeignKey('speech_recordings.id', ondelete='CASCADE'), nullable=False)
    overall_score = Column(DECIMAL(5, 2), nullable=False)
    clarity_score = Column(DECIMAL(5, 2), nullable=False)
    grammar_score = Column(DECIMAL(5, 2), nullable=False)
    vocabulary_score = Column(DECIMAL(5, 2), nullable=False)
    fluency_score = Column(DECIMAL(5, 2), nullable=False)
    detailed_feedback = Column(Text)

    recording = relationship('SpeechRecording', back_populates='speech_grades')
    improvements = relationship('SpeechGradeImprovement', back_populates='grade', cascade='all, delete-orphan')
    strengths = relationship('SpeechGradeStrength', back_populates='grade', cascade='all, delete-orphan')


class SpeechGradeImprovement(BaseModel):
    __tablename__ = "speech_grade_improvements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    grade_id = Column(Integer, ForeignKey('speech_grades.id', ondelete='CASCADE'), nullable=False)
    suggestion = Column(Text, nullable=False)
    category = Column(Enum(SpeechGradeImprovementCategory), default=SpeechGradeImprovementCategory.GENERAL, nullable=False)

    grade = relationship('SpeechGrade', back_populates='improvements')


class SpeechGradeStrength(BaseModel):
    __tablename__ = "speech_grade_strengths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    grade_id = Column(Integer, ForeignKey('speech_grades.id', ondelete='CASCADE'), nullable=False)
    strength = Column(Text, nullable=False)
    
    grade = relationship('SpeechGrade', back_populates='strengths')
