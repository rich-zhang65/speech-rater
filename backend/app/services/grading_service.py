from openai import OpenAI
from app.config import settings
import json
import re


class GradingService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def grade_speech(self, transcription: str) -> dict:
        """
        Grade speech quality using GPT-3.5 and provide detailed feedback.
        
        Args:
            transcription: The transcribed speech text
            
        Returns:
            Dictionary containing scores, strengths, improvements, and feedback
        """
        try:
            prompt = self._create_grading_prompt(transcription)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert speech coach and evaluator. Analyze speech transcriptions and provide constructive feedback with specific scores and actionable suggestions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse the response
            result_text = response.choices[0].message.content
            return self._parse_grading_response(result_text)
        
        except Exception as e:
            print(f"Error grading speech: {str(e)}")
            # Return default scores if API fails
            return self._get_default_grading()
    
    def _create_grading_prompt(self, transcription: str) -> str:
        """Create a detailed prompt for GPT to grade the speech."""
        return f"""Analyze the following speech transcription and provide a detailed evaluation:

TRANSCRIPTION:
"{transcription}"

Please provide your evaluation in the following JSON format:

{{
    "overall_score": <0-100>,
    "clarity_score": <0-100>,
    "grammar_score": <0-100>,
    "vocabulary_score": <0-100>,
    "fluency_score": <0-100>,
    "strengths": ["strength1", "strength2", "strength3"],
    "improvements": ["improvement1", "improvement2", "improvement3"],
    "detailed_feedback": "A paragraph with detailed, constructive feedback"
}}

Evaluation criteria:
- Clarity: How clear and articulate is the speech? Is it easy to understand?
- Grammar: Are sentences grammatically correct and well-structured?
- Vocabulary: Is the vocabulary appropriate, varied, and sophisticated?
- Fluency: How smooth and natural is the speech flow? Are there filler words or hesitations?
- Overall: Holistic assessment considering all factors

Provide specific, actionable feedback that will help the speaker improve."""
    
    def _parse_grading_response(self, response_text: str) -> dict:
        """Parse GPT response to extract grading information."""
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                
                # Validate and ensure all required fields exist
                return {
                    "overall_score": float(data.get("overall_score", 75)),
                    "clarity_score": float(data.get("clarity_score", 75)),
                    "grammar_score": float(data.get("grammar_score", 75)),
                    "vocabulary_score": float(data.get("vocabulary_score", 75)),
                    "fluency_score": float(data.get("fluency_score", 75)),
                    "strengths": data.get("strengths", [])[:5],  # Limit to 5
                    "improvements": data.get("improvements", [])[:5],  # Limit to 5
                    "detailed_feedback": data.get("detailed_feedback", "")
                }
        except Exception as e:
            print(f"Error parsing grading response: {str(e)}")
        
        return self._get_default_grading()
    
    def _get_default_grading(self) -> dict:
        """Return default grading when API fails or parsing fails."""
        return {
            "overall_score": 75.0,
            "clarity_score": 75.0,
            "grammar_score": 75.0,
            "vocabulary_score": 75.0,
            "fluency_score": 75.0,
            "strengths": [
                "Speech was recorded successfully",
                "Transcription completed"
            ],
            "improvements": [
                "Unable to provide detailed analysis at this time",
                "Please try again"
            ],
            "detailed_feedback": "We encountered an issue analyzing your speech in detail. Please try again."
        }

