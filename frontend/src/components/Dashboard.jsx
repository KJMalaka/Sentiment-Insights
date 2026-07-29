import { Eye, ThumbsUp, Users, Calendar } from 'lucide-react'
import AmbassadorScore from './AmbassadorScore'
import SentimentCharts from './SentimentCharts'
import CommentsTable from './CommentsTable'
import ReportExport from './ReportExport'

function formatCompactNumber(num) {
  if (num === undefined || num === null) return '0'
  return new Intl.NumberFormat('en-US', { notation: 'compact', maximumFractionDigits: 1 }).format(num)
}

function formatDate(isoString) {
  if (!isoString) return null
  try {
    return new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day: 'numeric' }).format(new Date(isoString))
  } catch {
    return null
  }
}

export default function Dashboard({ data }) {
  const { video_data, insights, comments, platform } = data
  const publishDate = formatDate(video_data.publish_date)

  return (
    <div className="space-y-8 animate-in fade-in duration-500" id="dashboard-content">

      {/* Header section */}
      <div className="bg-navy-800 rounded-xl border border-navy-700 overflow-hidden">
        {video_data.thumbnail_url && (
          <div className="relative w-full h-48 md:h-64 overflow-hidden">
            <img
              src={video_data.thumbnail_url}
              alt={video_data.title}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-navy-800 via-navy-800/60 to-transparent" />
            {platform && (
              <span className="absolute top-4 left-4 bg-navy-900/80 backdrop-blur text-amber-400 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full border border-navy-700">
                {platform}
              </span>
            )}
          </div>
        )}

        <div className="p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="min-w-0">
            <h2 className="text-2xl font-bold text-gray-100 leading-tight">{video_data.title}</h2>
            <div className="flex flex-wrap items-center gap-x-4 gap-y-2 mt-3 text-sm text-navy-300">
              <span className="font-semibold text-gray-200">{video_data.channel_name}</span>
              <span className="flex items-center gap-1.5">
                <Eye size={14} className="text-navy-400" /> {formatCompactNumber(video_data.view_count)} views
              </span>
              <span className="flex items-center gap-1.5">
                <ThumbsUp size={14} className="text-navy-400" /> {formatCompactNumber(video_data.like_count)}
              </span>
              {!!video_data.subscriber_count && (
                <span className="flex items-center gap-1.5">
                  <Users size={14} className="text-navy-400" /> {formatCompactNumber(video_data.subscriber_count)} subscribers
                </span>
              )}
              {publishDate && (
                <span className="flex items-center gap-1.5">
                  <Calendar size={14} className="text-navy-400" /> {publishDate}
                </span>
              )}
            </div>
          </div>
          <ReportExport data={data} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* Left Column - Score & Themes */}
        <div className="space-y-8 lg:col-span-1">
          <AmbassadorScore scoreData={insights.ambassador_score} />

          <div className="bg-navy-800 rounded-xl p-6 border border-navy-700">
            <h3 className="text-lg font-semibold text-amber-400 mb-4 border-b border-navy-700 pb-2">Top Themes</h3>
            <ul className="space-y-3">
              {insights.top_themes.map((theme, i) => (
                <li key={i} className="flex justify-between items-center bg-navy-900 px-4 py-2 rounded-lg">
                  <span className="capitalize">{theme.theme}</span>
                  <span className="text-amber-500 font-bold bg-amber-500/10 px-2 rounded-md">{theme.count}</span>
                </li>
              ))}
              {insights.top_themes.length === 0 && (
                <li className="text-navy-300 italic">No themes detected.</li>
              )}
            </ul>
          </div>

          <div className="bg-navy-800 rounded-xl p-6 border border-navy-700">
            <h3 className="text-lg font-semibold text-amber-400 mb-2 border-b border-navy-700 pb-2">Nuance & Controversy</h3>
            <p className="text-navy-300 text-sm mb-4">
              Agreement across layers: <span className="text-gray-100 font-bold">{insights.agreement_rate}%</span>
            </p>
            {insights.nuanced_examples.length > 0 ? (
              <div className="space-y-3">
                <p className="text-xs text-navy-300 uppercase tracking-wider font-semibold mb-2">Examples of mixed/sarcastic comments:</p>
                {insights.nuanced_examples.map((ex, i) => (
                  <div key={i} className="bg-navy-900 p-3 rounded-lg text-sm border-l-2 border-amber-500">
                    "{ex}"
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-navy-300 italic text-sm">No significant controversial or sarcastic comments detected.</p>
            )}
          </div>
        </div>

        {/* Right Column - Charts & Table */}
        <div className="space-y-8 lg:col-span-2">
          <SentimentCharts distributions={insights.distributions} />
          <CommentsTable comments={comments} />
        </div>

      </div>
    </div>
  )
}
