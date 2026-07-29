import { useState } from 'react'
import { Layers } from 'lucide-react'
import UrlInput from './components/UrlInput'
import Dashboard from './components/Dashboard'
import AnalyzingProgress from './components/AnalyzingProgress'

function App() {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  const analyzeUrl = async (url) => {
    setLoading(true)
    setError(null)
    setData(null)
    
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to analyze video')
      }
      
      const result = await response.json()
      setData(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-8 max-w-7xl mx-auto">
      <header className="mb-12 text-center">
        <div className="inline-flex items-center gap-2 bg-navy-800 border border-navy-700 text-amber-400 text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-5">
          <Layers size={14} />
          3-Layer Sentiment Pipeline
        </div>
        <h1 className="text-4xl md:text-5xl font-black bg-gradient-to-br from-gray-50 via-gray-100 to-amber-400 bg-clip-text text-transparent mb-4 tracking-tight leading-tight">
          Social Sentiment & Brand Ambassador Fit Analyzer
        </h1>
        <p className="text-navy-300 max-w-2xl mx-auto opacity-80">
          Paste a video URL to run VADER, a classic ML model, and a Groq-powered LLM across every comment — then get a brand ambassador fit score.
        </p>
      </header>

      <main>
        <UrlInput onSubmit={analyzeUrl} loading={loading} error={error} />

        {loading && <AnalyzingProgress />}

        {data && !loading && (
          <div className="mt-12 fade-in">
            <Dashboard data={data} />
          </div>
        )}
      </main>
    </div>
  )
}

export default App
