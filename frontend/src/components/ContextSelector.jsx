/**
 * Context Selector Component
 * Allows users to specify site context for context-aware risk scoring
 */

import React, { useState } from 'react'

export default function ContextSelector({ onContextChange, defaultContext = 'marketing' }) {
  const [context, setContext] = useState(defaultContext)

  const contexts = [
    {
      value: 'marketing',
      label: '📢 Marketing Site',
      description: 'Public-facing content, general audience',
      icon: '📢',
    },
    {
      value: 'authentication',
      label: '🔐 Authentication',
      description: 'Login, user accounts, sensitive access',
      icon: '🔐',
    },
    {
      value: 'ecommerce',
      label: '🛒 E-commerce',
      description: 'Payment processing, customer data',
      icon: '🛒',
    },
    {
      value: 'internal',
      label: '🏢 Internal',
      description: 'Corporate systems, employee access',
      icon: '🏢',
    },
  ]

  const handleContextChange = (newContext) => {
    setContext(newContext)
    onContextChange?.(newContext)
  }

  const selectedContextData = contexts.find(c => c.value === context)

  return (
    <div className="flex flex-col gap-4">
      {/* Label */}
      <div>
        <label className="text-sm font-semibold text-slate-200">Site Context</label>
        <p className="text-xs text-slate-400 mt-1">
          Context affects risk scoring weights and security recommendations
        </p>
      </div>

      {/* Grid of context buttons */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {contexts.map(ctx => (
          <button
            key={ctx.value}
            onClick={() => handleContextChange(ctx.value)}
            className={`relative p-3 rounded-lg border-2 transition-all duration-300 group ${
              context === ctx.value
                ? 'bg-gradient-to-br from-system-purple/20 to-system-violet/10 border-system-purple'
                : 'bg-slate-800/50 border-slate-700 hover:border-slate-600 hover:bg-slate-800'
            }`}
          >
            {/* Selected indicator */}
            {context === ctx.value && (
              <div className="absolute top-1 right-1 w-3 h-3 rounded-full bg-system-purple animate-pulse" />
            )}

            {/* Icon */}
            <div className="text-2xl mb-2">{ctx.icon}</div>

            {/* Label */}
            <p className="text-xs font-semibold text-slate-200 text-left">{ctx.label.split(' ')[1]}</p>

            {/* Tooltip on hover */}
            <div
              className={`absolute -bottom-12 left-1/2 transform -translate-x-1/2 bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs text-slate-300 whitespace-nowrap pointer-events-none transition-opacity duration-300 ${
                context === ctx.value ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'
              }`}
            >
              {ctx.description}
            </div>
          </button>
        ))}
      </div>

      {/* Current selection info */}
      {selectedContextData && (
        <div className="mt-2 p-3 rounded-lg bg-slate-800/50 border border-slate-700">
          <p className="text-xs font-semibold text-slate-300 mb-1">
            Selected: {selectedContextData.label}
          </p>
          <p className="text-xs text-slate-400">{selectedContextData.description}</p>
        </div>
      )}
    </div>
  )
}
