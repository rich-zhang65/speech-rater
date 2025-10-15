from pydantic import Field
from typing import List

from app.schemas.base import BaseSchema

class SpeechGradingResponse(BaseSchema):
    overall_score: float = Field(..., ge=0, le=100, description="Overall speech quality score (0-100)")
    clarity_score: float = Field(..., ge=0, le=100, description="Clarity and articulation score")
    grammar_score: float = Field(..., ge=0, le=100, description="Grammar and structure score")
    vocabulary_score: float = Field(..., ge=0, le=100, description="Vocabulary richness score")
    fluency_score: float = Field(..., ge=0, le=100, description="Fluency and coherence score")
    strengths: List[str] = Field(..., description="Key strengths identified")
    improvements: List[str] = Field(..., description="Suggested improvements")
    detailed_feedback: str = Field(..., description="Detailed feedback on the speech")


class SpeechAnalysisResponse(BaseSchema):
    transcription: str = Field(..., description="Transcribed text from audio")
    word_count: int = Field(..., description="Number of words in transcription")
    overall_score: float = Field(..., ge=0, le=100, description="Overall speech quality score")
    clarity_score: float = Field(..., ge=0, le=100, description="Clarity score")
    grammar_score: float = Field(..., ge=0, le=100, description="Grammar score")
    vocabulary_score: float = Field(..., ge=0, le=100, description="Vocabulary score")
    fluency_score: float = Field(..., ge=0, le=100, description="Fluency score")
    strengths: List[str] = Field(..., description="Key strengths")
    improvements: List[str] = Field(..., description="Suggested improvements")
    detailed_feedback: str = Field(..., description="Detailed feedback")

