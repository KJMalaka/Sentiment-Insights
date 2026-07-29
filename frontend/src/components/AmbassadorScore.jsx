import clsx from 'clsx'

export default function AmbassadorScore({ scoreData }) {
  const { score, band, rationale } = scoreData

  // Determine colors based on score
  let colorClass = 'text-green-500'
  let bgClass = 'bg-green-500/10'
  let borderClass = 'border-green-500'

  if (score < 25) {
    colorClass = 'text-red-500'
    bgClass = 'bg-red-500/10'
    borderClass = 'border-red-500'
  } else if (score < 50) {
    colorClass = 'text-orange-500'
    bgClass = 'bg-orange-500/10'
    borderClass = 'border-orange-500'
  } else if (score < 75) {
    colorClass = 'text-amber-400'
    bgClass = 'bg-amber-400/10'
    borderClass = 'border-amber-400'
  }

  const size = 168
  const stroke = 14
  const radius = (size - stroke) / 2
  const circumference = radius * 2 * Math.PI
  const strokeDashoffset = circumference - (Math.max(0, Math.min(100, score)) / 100) * circumference

  return (
    <div className={clsx("rounded-xl p-6 border text-center flex flex-col items-center justify-center relative overflow-hidden", borderClass, bgClass)}>
      {/* Background decoration */}
      <div className={clsx("absolute -right-4 -top-4 w-24 h-24 rounded-full blur-2xl opacity-20", bgClass.replace('/10', ''))} />
      <div className={clsx("absolute -left-4 -bottom-4 w-32 h-32 rounded-full blur-3xl opacity-20", bgClass.replace('/10', ''))} />

      <h3 className="text-navy-300 font-semibold uppercase tracking-widest text-sm mb-6 z-10">Brand Ambassador Fit</h3>

      <div className="relative z-10 mb-6" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            stroke="currentColor"
            className="text-navy-700"
            fill="transparent"
            strokeWidth={stroke}
            r={radius}
            cx={size / 2}
            cy={size / 2}
          />
          <circle
            stroke="currentColor"
            className={clsx(colorClass, "transition-[stroke-dashoffset] duration-1000 ease-out")}
            fill="transparent"
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={`${circumference} ${circumference}`}
            strokeDashoffset={strokeDashoffset}
            r={radius}
            cx={size / 2}
            cy={size / 2}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={clsx("text-5xl font-black tabular-nums tracking-tighter", colorClass)}>
            {score}
          </span>
          <span className="text-navy-400 text-xs font-bold uppercase tracking-wider mt-1">out of 100</span>
        </div>
      </div>

      <div className={clsx("px-4 py-1 rounded-full text-sm font-bold border mb-6 z-10", colorClass, borderClass)}>
        {band}
      </div>

      <p className="text-gray-200 text-sm leading-relaxed max-w-sm text-left border-t border-navy-700/50 pt-4 z-10">
        {rationale}
      </p>
    </div>
  )
}
