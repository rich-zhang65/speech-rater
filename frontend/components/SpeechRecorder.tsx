'use client'

import { useState, useRef, useEffect } from 'react'
import { analyzeSpeech } from '@/lib/api/speech'
import { SpeechAnalysis } from '@/lib/types/speech'

interface SpeechRecorderProps {
  onAnalysisComplete: (analysis: SpeechAnalysis) => void
  loading: boolean
  setLoading: (loading: boolean) => void
}

export default function SpeechRecorder({ onAnalysisComplete, loading, setLoading }: SpeechRecorderProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [audioURL, setAudioURL] = useState<string | null>(null)
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [duration, setDuration] = useState(0)
  const [error, setError] = useState<string | null>(null)
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const timerRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
      if (audioURL) URL.revokeObjectURL(audioURL)
    }
  }, [audioURL])

  const startRecording = async () => {
    try {
      setError(null)
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/wav' })
        const url = URL.createObjectURL(blob)
        setAudioURL(url)
        setAudioBlob(blob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
      setDuration(0)

      // Start timer
      timerRef.current = setInterval(() => {
        setDuration(prev => prev + 1)
      }, 1000)
    } catch (err) {
      setError('Failed to access microphone. Please ensure microphone permissions are granted.')
      console.error('Error accessing microphone:', err)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      
      if (timerRef.current) {
        clearInterval(timerRef.current)
        timerRef.current = null
      }
    }
  }

  const handleAnalyze = async () => {
    if (!audioBlob) return

    setLoading(true)
    setError(null)

    try {
      const analysis = await analyzeSpeech(audioBlob)
      onAnalysisComplete(analysis)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze speech')
      setLoading(false)
    }
  }

  const handleReset = () => {
    setAudioURL(null)
    setAudioBlob(null)
    setDuration(0)
    setError(null)
  }

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <div className="text-center">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {!audioURL ? (
          <div className="space-y-6">
            <div className="flex justify-center">
              <div className={`w-32 h-32 rounded-full flex items-center justify-center ${
                isRecording ? 'bg-red-500 animate-pulse' : 'bg-blue-500'
              }`}>
                <svg 
                  className="w-16 h-16 text-white" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
                  />
                </svg>
              </div>
            </div>

            {isRecording && (
              <div className="text-3xl font-bold text-gray-800">
                {formatDuration(duration)}
              </div>
            )}

            <div>
              {!isRecording ? (
                <button
                  onClick={startRecording}
                  className="px-8 py-4 bg-blue-600 text-white rounded-full font-semibold text-lg hover:bg-blue-700 transition-colors shadow-lg"
                >
                  Start Recording
                </button>
              ) : (
                <button
                  onClick={stopRecording}
                  className="px-8 py-4 bg-red-600 text-white rounded-full font-semibold text-lg hover:bg-red-700 transition-colors shadow-lg"
                >
                  Stop Recording
                </button>
              )}
            </div>

            <p className="text-gray-600 text-sm">
              {isRecording 
                ? 'Recording in progress... Click "Stop Recording" when done.'
                : 'Click the button above to start recording your speech.'
              }
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-center">
              <div className="w-32 h-32 rounded-full bg-green-500 flex items-center justify-center">
                <svg 
                  className="w-16 h-16 text-white" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M5 13l4 4L19 7" 
                  />
                </svg>
              </div>
            </div>

            <div>
              <p className="text-lg font-medium text-gray-800 mb-2">
                Recording Complete
              </p>
              <p className="text-gray-600">
                Duration: {formatDuration(duration)}
              </p>
            </div>

            <audio controls src={audioURL} className="w-full" />

            <div className="flex gap-4 justify-center">
              <button
                onClick={handleReset}
                className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
              >
                Record Again
              </button>
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Analyzing...
                  </span>
                ) : (
                  'Analyze Speech'
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

