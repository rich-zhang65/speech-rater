'use client'

import { useState } from 'react'
import SpeechRecorder from '@/components/SpeechRecorder'
import ResultsDisplay from '@/components/ResultsDisplay'
import Header from '@/components/Header'
import { SpeechAnalysis } from '@/lib/types/speech'

export default function Home() {
  const [analysis, setAnalysis] = useState<SpeechAnalysis | null>(null)
  const [loading, setLoading] = useState(false)

  const handleAnalysisComplete = (result: SpeechAnalysis) => {
    setAnalysis(result)
    setLoading(false)
  }

  const handleNewRecording = () => {
    setAnalysis(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              Speech Rater
            </h1>
            <p className="text-xl text-gray-600">
              Record your speech and get instant AI-powered feedback
            </p>
          </div>

          {!analysis ? (
            <SpeechRecorder 
              onAnalysisComplete={handleAnalysisComplete}
              loading={loading}
              setLoading={setLoading}
            />
          ) : (
            <ResultsDisplay 
              analysis={analysis}
              onNewRecording={handleNewRecording}
            />
          )}
        </div>
      </main>

      <footer className="mt-16 py-8 text-center text-gray-600 border-t">
        <p>© 2024 Speech Rater. Powered by OpenAI Whisper & GPT-3.5.</p>
      </footer>
    </div>
  )
}
