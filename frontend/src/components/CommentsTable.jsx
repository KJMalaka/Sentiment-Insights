import { useState, useMemo } from 'react'
import { Filter } from 'lucide-react'

export default function CommentsTable({ comments }) {
  const [filter, setFilter] = useState('all') // all, positive, neutral, negative, controversial

  const filteredComments = useMemo(() => {
    if (filter === 'all') return comments
    if (filter === 'controversial') {
      return comments.filter(c => c.groq.is_sarcastic || c.groq.is_mixed)
    }
    // Filter by majority vote or groq
    return comments.filter(c => c.groq.label === filter)
  }, [comments, filter])

  const LabelBadge = ({ label }) => {
    let colorClass = 'bg-gray-500/20 text-gray-300 border-gray-500/30'
    if (label === 'positive') colorClass = 'bg-green-500/20 text-green-400 border-green-500/30'
    if (label === 'negative') colorClass = 'bg-red-500/20 text-red-400 border-red-500/30'
    
    return (
      <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider border ${colorClass}`}>
        {label}
      </span>
    )
  }

  return (
    <div className="bg-navy-800 rounded-xl p-6 border border-navy-700 h-[32rem] flex flex-col">
      <div className="flex justify-between items-center mb-4 pb-2 border-b border-navy-700">
        <h3 className="text-lg font-semibold text-amber-400">Raw Comments</h3>
        
        <div className="flex items-center gap-2">
          <Filter size={16} className="text-navy-400" />
          <select 
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="bg-navy-900 border border-navy-700 text-sm rounded-md px-2 py-1 text-gray-200 focus:outline-none focus:border-amber-400"
          >
            <option value="all">All Comments</option>
            <option value="positive">Positive (Groq)</option>
            <option value="neutral">Neutral (Groq)</option>
            <option value="negative">Negative (Groq)</option>
            <option value="controversial">Nuanced / Sarcastic</option>
          </select>
        </div>
      </div>
      
      <div className="overflow-y-auto flex-1 pr-2">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="text-navy-400 text-xs uppercase tracking-wider sticky top-0 bg-navy-800 z-10 shadow-sm">
              <th className="py-3 px-4 w-1/2">Comment Text</th>
              <th className="py-3 px-4">VADER</th>
              <th className="py-3 px-4">Classic ML</th>
              <th className="py-3 px-4">Groq LLM</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-navy-700">
            {filteredComments.map((c, i) => (
              <tr key={i} className="hover:bg-navy-700/30 transition-colors group">
                <td className="py-3 px-4 text-sm text-gray-300">
                  <div className="line-clamp-2 group-hover:line-clamp-none">{c.text}</div>
                  {c.groq.themes?.length > 0 && (
                    <div className="mt-2 flex gap-1">
                      {c.groq.themes.map((t, idx) => (
                        <span key={idx} className="bg-navy-900 text-amber-500/80 text-[10px] px-1.5 py-0.5 rounded border border-navy-700">
                          {t}
                        </span>
                      ))}
                    </div>
                  )}
                </td>
                <td className="py-3 px-4"><LabelBadge label={c.vader.label} /></td>
                <td className="py-3 px-4"><LabelBadge label={c.sklearn.label} /></td>
                <td className="py-3 px-4">
                  <div className="flex flex-col gap-1 items-start">
                    <LabelBadge label={c.groq.label} />
                    {(c.groq.is_sarcastic || c.groq.is_mixed) && (
                      <span className="text-[10px] text-amber-500 italic">
                        {c.groq.is_sarcastic ? 'Sarcastic' : 'Mixed'}
                      </span>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {filteredComments.length === 0 && (
              <tr>
                <td colSpan="4" className="py-8 text-center text-navy-400 italic">
                  No comments match this filter.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
