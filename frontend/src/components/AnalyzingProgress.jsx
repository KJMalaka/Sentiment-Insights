import { useEffect, useState } from 'react'
import { Search, MessageSquare, BarChart3, Sparkles, Check } from 'lucide-react'

const STEPS = [
  { label: 'Fetching video & comments', icon: Search, duration: 1800 },
  { label: 'Running VADER (rule-based)', icon: BarChart3, duration: 1400 },
  { label: 'Running Classic ML model', icon: BarChart3, duration: 1400 },
  { label: 'Querying Groq LLM for nuance', icon: Sparkles, duration: 2600 },
]

export default function AnalyzingProgress() {
  const [activeStep, setActiveStep] = useState(0)

  useEffect(() => {
    if (activeStep >= STEPS.length - 1) return
    const timer = setTimeout(() => setActiveStep((s) => s + 1), STEPS[activeStep].duration)
    return () => clearTimeout(timer)
  }, [activeStep])

  return (
    <div className="w-full max-w-2xl mx-auto mt-8 bg-navy-800 border border-navy-700 rounded-xl p-6 fade-in">
      <p className="text-xs uppercase tracking-widest text-navy-300 font-semibold mb-5">Analyzing</p>
      <div className="space-y-4">
        {STEPS.map((step, i) => {
          const Icon = step.icon
          const isDone = i < activeStep
          const isActive = i === activeStep
          return (
            <div key={step.label} className="flex items-center gap-3">
              <div
                className={`flex items-center justify-center w-8 h-8 rounded-full border shrink-0 transition-colors duration-300 ${
                  isDone
                    ? 'bg-amber-500/20 border-amber-500 text-amber-400'
                    : isActive
                    ? 'bg-amber-500 border-amber-500 text-navy-900'
                    : 'bg-navy-900 border-navy-700 text-navy-500'
                }`}
              >
                {isDone ? <Check size={16} /> : <Icon size={16} className={isActive ? 'animate-pulse-soft' : ''} />}
              </div>
              <span
                className={`text-sm transition-colors duration-300 ${
                  isDone ? 'text-navy-300' : isActive ? 'text-gray-100 font-semibold' : 'text-navy-500'
                }`}
              >
                {step.label}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
