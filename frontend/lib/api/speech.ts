import { SpeechAnalysis } from '../types/speech'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function analyzeSpeech(audioBlob: Blob): Promise<SpeechAnalysis> {
  const formData = new FormData()
  formData.append('audio', audioBlob, 'recording.wav')

  const response = await fetch(`${API_URL}/api/speech/analyze`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to analyze speech' }))
    throw new Error(error.detail || 'Failed to analyze speech')
  }

  return response.json()
}

export async function gradeSpeechText(text: string): Promise<Omit<SpeechAnalysis, 'transcription' | 'word_count'>> {
  const response = await fetch(`${API_URL}/api/speech/grade`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to grade speech' }))
    throw new Error(error.detail || 'Failed to grade speech')
  }

  return response.json()
}

