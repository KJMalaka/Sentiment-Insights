import { useState } from 'react'
import { Search, Loader2, AlertCircle } from 'lucide-react'

export default function UrlInput({ onSubmit, loading, error }) {
  const [url, setUrl] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (url.trim()) {
      onSubmit(url.trim())
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <div className="absolute left-4 text-navy-700">
          <Search size={20} />
        </div>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste video URL here (e.g., YouTube)..."
          disabled={loading}
          className="w-full bg-navy-800 border border-navy-700 rounded-lg py-4 pl-12 pr-32 text-gray-100 placeholder-navy-700 focus:outline-none focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-colors disabled:opacity-50"
          required
        />
        <button
          type="submit"
          disabled={loading || !url.trim()}
          className="absolute right-2 bg-amber-500 hover:bg-amber-400 text-navy-900 font-bold py-2 px-6 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin mr-2" size={18} />
              Analyzing
            </>
          ) : (
            'Analyze'
          )}
        </button>
      </form>
      
      {error && (
        <div className="mt-4 bg-red-900/30 border border-red-500/50 text-red-200 p-4 rounded-lg flex items-start">
          <AlertCircle className="mr-3 mt-0.5 flex-shrink-0 text-red-400" size={20} />
          <p>{error}</p>
        </div>
      )}
    </div>
  )
}
