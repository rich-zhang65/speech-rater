export interface SpeechAnalysis {
  transcription: string
  word_count: number
  overall_score: number
  clarity_score: number
  grammar_score: number
  vocabulary_score: number
  fluency_score: number
  strengths: string[]
  improvements: string[]
  detailed_feedback: string
}

export interface RecordingState {
  isRecording: boolean
  audioBlob: Blob | null
  audioURL: string | null
  duration: number
}

