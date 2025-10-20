'use client'

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <svg 
              className="w-8 h-8 text-blue-600" 
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
            <span className="text-xl font-bold text-gray-800">Speech Rater</span>
          </div>
          
          <nav>
            {/* Auth0 login button will go here in future */}
            <button className="px-4 py-2 text-blue-600 hover:text-blue-700 font-medium border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors">
              Sign In
            </button>
          </nav>
        </div>
      </div>
    </header>
  )
}

