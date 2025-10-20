'use client'

import { SpeechAnalysis } from '@/lib/types/speech'

interface ResultsDisplayProps {
  analysis: SpeechAnalysis
  onNewRecording: () => void
}

export default function ResultsDisplay({ analysis, onNewRecording }: ResultsDisplayProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  const ScoreCircle = ({ score, label }: { score: number; label: string }) => (
    <div className="text-center">
      <div className={`w-24 h-24 rounded-full ${getScoreBgColor(score)} flex items-center justify-center mx-auto mb-2`}>
        <span className={`text-2xl font-bold ${getScoreColor(score)}`}>
          {score.toFixed(0)}
        </span>
      </div>
      <p className="text-sm text-gray-600">{label}</p>
    </div>
  )

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Overall Score</h2>
        <div className={`inline-flex items-center justify-center w-40 h-40 rounded-full ${getScoreBgColor(analysis.overall_score)}`}>
          <span className={`text-6xl font-bold ${getScoreColor(analysis.overall_score)}`}>
            {analysis.overall_score.toFixed(0)}
          </span>
        </div>
        <p className="mt-4 text-gray-600">
          {analysis.overall_score >= 80 && 'Excellent work!'}
          {analysis.overall_score >= 60 && analysis.overall_score < 80 && 'Good job! Room for improvement.'}
          {analysis.overall_score < 60 && 'Keep practicing! You\'ll improve.'}
        </p>
      </div>

      {/* Detailed Scores */}
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h3 className="text-xl font-bold text-gray-800 mb-6">Detailed Breakdown</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <ScoreCircle score={analysis.clarity_score} label="Clarity" />
          <ScoreCircle score={analysis.grammar_score} label="Grammar" />
          <ScoreCircle score={analysis.vocabulary_score} label="Vocabulary" />
          <ScoreCircle score={analysis.fluency_score} label="Fluency" />
        </div>
      </div>

      {/* Transcription */}
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Your Speech</h3>
        <div className="bg-gray-50 rounded-lg p-6">
          <p className="text-gray-700 leading-relaxed">{analysis.transcription}</p>
        </div>
        <p className="mt-3 text-sm text-gray-600">
          Word count: {analysis.word_count} words
        </p>
      </div>

      {/* Strengths */}
      {analysis.strengths.length > 0 && (
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Strengths
          </h3>
          <ul className="space-y-2">
            {analysis.strengths.map((strength, index) => (
              <li key={index} className="flex items-start gap-3">
                <span className="text-green-600 mt-1">✓</span>
                <span className="text-gray-700">{strength}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Improvements */}
      {analysis.improvements.length > 0 && (
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            Areas for Improvement
          </h3>
          <ul className="space-y-2">
            {analysis.improvements.map((improvement, index) => (
              <li key={index} className="flex items-start gap-3">
                <span className="text-blue-600 mt-1">→</span>
                <span className="text-gray-700">{improvement}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Detailed Feedback */}
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Detailed Feedback</h3>
        <p className="text-gray-700 leading-relaxed whitespace-pre-line">
          {analysis.detailed_feedback}
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center gap-4">
        <button
          onClick={onNewRecording}
          className="px-8 py-4 bg-blue-600 text-white rounded-full font-semibold text-lg hover:bg-blue-700 transition-colors shadow-lg"
        >
          Record Another Speech
        </button>
      </div>
    </div>
  )
}

