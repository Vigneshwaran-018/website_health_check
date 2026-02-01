/**
 * Security Pulse Visualization Component
 * A unique, animated risk score visualization that uses a "living system" metaphor
 * The intensity and color react to risk levels in real-time
 */

import React, { useState, useEffect } from 'react'

export default function SecurityPulseViz({ riskScore, riskLevel }) {
  if (!riskScore) return null

  const { score } = riskScore
  const [pulseIntensity, setPulseIntensity] = useState(1)
  const [coreColor, setCoreColor] = useState('#22c55e')
  const [fragmentCount, setFragmentCount] = useState(0)

  // Determine color based on risk level
  useEffect(() => {
    switch (riskLevel) {
      case 'LOW':
        setCoreColor('#22c55e')
        break
      case 'MEDIUM':
        setCoreColor('#f59e0b')
        break
      case 'HIGH':
        setCoreColor('#f97316')
        break
      case 'CRITICAL':
        setCoreColor('#dc2626')
        break
      default:
        setCoreColor('#94a3b8')
    }

    // Set pulse speed based on risk
    const speed = 100 + (100 - score) * 2
    const interval = setInterval(() => {
      setPulseIntensity(prev => {
        if (prev >= 1.5) return 1
        return prev + 0.05
      })
    }, speed)

    // Fragment count increases with danger
    const fragmentsAtRisk = Math.floor((100 - score) / 20)
    setFragmentCount(fragmentsAtRisk)

    return () => clearInterval(interval)
  }, [score, riskLevel])

  const getRadiusClass = () => {
    if (score >= 80) return 'w-16 h-16'
    if (score >= 60) return 'w-20 h-20'
    if (score >= 40) return 'w-24 h-24'
    return 'w-28 h-28'
  }

  const getAuraColor = () => {
    switch (riskLevel) {
      case 'LOW':
        return 'shadow-glow-green'
      case 'MEDIUM':
        return 'shadow-glow-green'
      case 'HIGH':
        return 'shadow-glow-red'
      case 'CRITICAL':
        return 'shadow-glow-red'
      default:
        return 'shadow-glow-blue'
    }
  }

  // Generate fragment positions around the core
  const fragments = Array.from({ length: fragmentCount }).map((_, i) => {
    const angle = (i / fragmentCount) * Math.PI * 2
    const distance = 60 + Math.random() * 20
    const x = Math.cos(angle) * distance
    const y = Math.sin(angle) * distance
    const duration = 2 + Math.random() * 2

    return (
      <div
        key={`fragment-${i}`}
        className="absolute rounded-full"
        style={{
          width: '8px',
          height: '8px',
          left: `calc(50% + ${x}px)`,
          top: `calc(50% + ${y}px)`,
          backgroundColor: coreColor,
          opacity: 0.6,
          animation: `float ${duration}s ease-in-out infinite`,
          boxShadow: `0 0 10px ${coreColor}`,
        }}
      />
    )
  })

  return (
    <div className="flex flex-col items-center justify-center gap-6">
      {/* Main Pulse Core */}
      <div className="relative w-40 h-40 flex items-center justify-center">
        {/* Outer aura rings */}
        <div
          className={`absolute rounded-full ${getAuraColor()} transition-all duration-300`}
          style={{
            width: `${120 + pulseIntensity * 20}px`,
            height: `${120 + pulseIntensity * 20}px`,
            opacity: 0.2,
          }}
        />

        <div
          className={`absolute rounded-full ${getAuraColor()} transition-all duration-300`}
          style={{
            width: `${80 + pulseIntensity * 15}px`,
            height: `${80 + pulseIntensity * 15}px`,
            opacity: 0.4,
          }}
        />

        {/* Central core shield */}
        <div
          className={`absolute ${getRadiusClass()} rounded-full transition-all duration-300`}
          style={{
            backgroundColor: coreColor,
            opacity: 0.8 + pulseIntensity * 0.2,
            boxShadow: `0 0 ${20 + pulseIntensity * 10}px ${coreColor}`,
          }}
        />

        {/* Score display in center */}
        <div className="absolute flex flex-col items-center justify-center z-10">
          <span
            className="text-4xl font-black transition-all duration-300"
            style={{ color: coreColor }}
          >
            {Math.round(score)}
          </span>
          <span className="text-xs text-slate-400 font-mono">SECURITY</span>
        </div>

        {/* Fragments (threat indicators) */}
        {fragments}

        {/* Threat constellation lines */}
        {fragmentCount > 0 && (
          <svg
            className="absolute inset-0 w-full h-full pointer-events-none"
            style={{ opacity: 0.3 }}
          >
            {Array.from({ length: fragmentCount }).map((_, i) => {
              const angle = (i / fragmentCount) * Math.PI * 2
              const distance = 60 + Math.random() * 20
              const x = 80 + Math.cos(angle) * distance
              const y = 80 + Math.sin(angle) * distance
              return (
                <line
                  key={`line-${i}`}
                  x1="80"
                  y1="80"
                  x2={x}
                  y2={y}
                  stroke={coreColor}
                  strokeWidth="1"
                  opacity="0.5"
                />
              )
            })}
          </svg>
        )}
      </div>

      {/* Status Indicators Below */}
      <div className="flex items-center gap-4 text-sm">
        <div className="flex items-center gap-2">
          <div
            className="w-3 h-3 rounded-full animate-pulse"
            style={{ backgroundColor: coreColor }}
          />
          <span className="text-slate-300">{riskLevel} RISK</span>
        </div>

        {/* Threat Level Bars */}
        <div className="flex items-center gap-1">
          {Array.from({ length: 5 }).map((_, i) => (
            <div
              key={`bar-${i}`}
              className="w-1 transition-all duration-300"
              style={{
                height: i < Math.ceil(score / 20) ? '16px' : '4px',
                backgroundColor:
                  i < Math.ceil(score / 20) ? coreColor : '#475569',
              }}
            />
          ))}
        </div>
      </div>

      {/* Risk Interpretation */}
      <div className="text-center text-xs text-slate-400 mt-2">
        {score >= 80 && '✅ System is resilient and well-protected'}
        {score >= 60 && score < 80 && '🟡 System has acceptable protection'}
        {score >= 40 && score < 60 && '⚠️ System needs attention'}
        {score < 40 && '🚨 System is critically vulnerable'}
      </div>
    </div>
  )
}
