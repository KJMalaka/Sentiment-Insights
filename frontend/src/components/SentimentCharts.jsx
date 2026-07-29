import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, Cell } from 'recharts'

export default function SentimentCharts({ distributions }) {
  // Convert dict to array for recharts
  const data = [
    {
      name: 'VADER (Rule-based)',
      Positive: distributions.vader.positive,
      Neutral: distributions.vader.neutral,
      Negative: distributions.vader.negative,
    },
    {
      name: 'Classic ML (LogReg)',
      Positive: distributions.sklearn.positive,
      Neutral: distributions.sklearn.neutral,
      Negative: distributions.sklearn.negative,
    },
    {
      name: 'Groq LLM',
      Positive: distributions.groq.positive,
      Neutral: distributions.groq.neutral,
      Negative: distributions.groq.negative,
    }
  ]

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-navy-900 border border-navy-700 p-3 rounded-lg shadow-xl">
          <p className="text-gray-100 font-bold mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={`item-${index}`} style={{ color: entry.color }} className="text-sm font-semibold">
              {entry.name}: {entry.value}%
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className="bg-navy-800 rounded-xl p-6 border border-navy-700 h-80">
      <h3 className="text-lg font-semibold text-amber-400 mb-4 border-b border-navy-700 pb-2">Sentiment Distribution Across Layers</h3>
      <ResponsiveContainer width="100%" height="80%">
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: -20, bottom: 5 }}
        >
          <XAxis dataKey="name" stroke="#5c6b8a" tick={{ fill: '#5c6b8a', fontSize: 12 }} />
          <YAxis stroke="#5c6b8a" tick={{ fill: '#5c6b8a', fontSize: 12 }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ paddingTop: '10px' }} />
          <Bar dataKey="Positive" stackId="a" fill="#10b981" radius={[0, 0, 4, 4]} />
          <Bar dataKey="Neutral" stackId="a" fill="#64748b" />
          <Bar dataKey="Negative" stackId="a" fill="#ef4444" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
