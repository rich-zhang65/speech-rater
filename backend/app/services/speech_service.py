import os
import tempfile
from openai import OpenAI
from app.config import settings


class SpeechService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def transcribe_audio(self, audio_data: bytes, filename: str) -> str:
        """
        Transcribe audio using OpenAI Whisper API.
        
        Args:
            audio_data: Raw audio file bytes
            filename: Original filename for proper extension handling
            
        Returns:
            Transcribed text
        """
        try:
            # Create a temporary file to store the audio
            # Whisper API requires a file-like object
            suffix = os.path.splitext(filename)[1] or '.wav'
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            try:
                # Open the file and send to Whisper
                with open(temp_audio_path, 'rb') as audio_file:
                    transcription = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text"
                    )
                
                return transcription.strip() if isinstance(transcription, str) else transcription.text.strip()
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)
        
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")

