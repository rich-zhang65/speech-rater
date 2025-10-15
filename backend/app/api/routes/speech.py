from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.speech_service import SpeechService
from app.services.grading_service import GradingService
from app.schemas.speech import SpeechAnalysisResponse, SpeechGradingResponse
from typing import Optional

router = APIRouter(prefix="/speech")

speech_service = SpeechService()
grading_service = GradingService()

@router.post("/analyze", response_model=SpeechAnalysisResponse)
async def analyze_speech(
    audio: UploadFile = File(...),
    user_id: Optional[str] = None
):
    """
    Analyze speech from audio file using OpenAI Whisper.
    Returns transcription and basic analysis.
    """
    try:
        # Validate audio file
        if not audio.content_type or not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Invalid audio file format")
        
        # Read audio file
        audio_data = await audio.read()
        
        # Transcribe using Whisper
        transcription = await speech_service.transcribe_audio(audio_data, audio.filename)
        
        if not transcription:
            raise HTTPException(status_code=500, detail="Failed to transcribe audio")
        
        # Get speech analysis and grading
        grading_result = await grading_service.grade_speech(transcription)
        
        return SpeechAnalysisResponse(
            transcription=transcription,
            word_count=len(transcription.split()),
            **grading_result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing speech: {str(e)}")


@router.post("/grade", response_model=SpeechGradingResponse)
async def grade_speech_text(text: dict):
    """
    Grade speech quality from transcribed text.
    Accepts JSON with 'text' field.
    """
    try:
        transcription = text.get("text", "")
        
        if not transcription or len(transcription.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Grade the speech
        grading_result = await grading_service.grade_speech(transcription)
        
        return SpeechGradingResponse(**grading_result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error grading speech: {str(e)}")
