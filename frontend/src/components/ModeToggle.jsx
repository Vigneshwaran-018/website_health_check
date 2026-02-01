/**
 * Attacker/Defender Mode Toggle
 * Animated switch to toggle between perspectives with visual feedback
 */

import React, { useState, useEffect } from 'react'

export default function ModeToggle({ onModeChange, defaultMode = 'defender' }) {
  const [mode, setMode] = useState(defaultMode)
  const [isAnimating, setIsAnimating] = useState(false)

  const handleToggle = () => {
    setIsAnimating(true)
    const newMode = mode === 'defender' ? 'attacker' : 'defender'
    setMode(newMode)
    onModeChange?.(newMode)

    setTimeout(() => setIsAnimating(false), 300)
  }

  const isDefender = mode === 'defender'

  return (
    <div className="flex items-center gap-4">
      {/* Label */}
      <div className="flex items-center gap-2">
        <span
          className={`text-sm font-semibold transition-colors duration-300 ${
            isDefender ? 'text-defend-cyan' : 'text-slate-400'
          }`}
        >
          🛡️ Defender
        </span>
        <span className="text-slate-400 text-xs">|</span>
        <span
          className={`text-sm font-semibold transition-colors duration-300 ${
            !isDefender ? 'text-attack-crimson' : 'text-slate-400'
          }`}
        >
          ⚔️ Attacker
        </span>
      </div>

      {/* Toggle Switch */}
      <button
        onClick={handleToggle}
        className="relative inline-flex h-8 w-16 items-center rounded-full bg-slate-800 border border-slate-700 cursor-pointer transition-all duration-300 hover:border-slate-600"
        aria-label={`Switch to ${isDefender ? 'Attacker' : 'Defender'} view`}
      >
        {/* Animated background */}
        <div
          className={`absolute inset-1 rounded-full transition-all duration-300 ${
            isDefender
              ? 'bg-gradient-to-r from-defend-cyan/20 to-defend-blue/10'
              : 'bg-gradient-to-r from-attack-crimson/20 to-attack-scarlet/10'
          }`}
        />

        {/* Toggle thumb */}
        <div
          className={`relative w-6 h-6 rounded-full transition-all duration-300 ${
            isAnimating ? 'scale-110' : 'scale-100'
          } ${
            isDefender
              ? 'translate-x-1 bg-gradient-to-br from-defend-cyan to-defend-blue shadow-glow-blue'
              : 'translate-x-9 bg-gradient-to-br from-attack-crimson to-attack-scarlet shadow-glow-red'
          }`}
        />

        {/* Icons */}
        <span
          className={`absolute left-1.5 text-xs transition-opacity duration-300 ${
            isDefender ? 'opacity-100' : 'opacity-30'
          }`}
        >
          🛡️
        </span>
        <span
          className={`absolute right-1.5 text-xs transition-opacity duration-300 ${
            !isDefender ? 'opacity-100' : 'opacity-30'
          }`}
        >
          ⚔️
        </span>
      </button>

      {/* Mode Description */}
      <div className="text-xs text-slate-400 min-w-[120px]">
        {isDefender ? (
          <p>Prioritized fixes & mitigation</p>
        ) : (
          <p>Exploitation & attack surface</p>
        )}
      </div>
    </div>
  )
}
