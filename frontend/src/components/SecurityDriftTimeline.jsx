/**
 * Security Drift Timeline
 * Visualizes changes in security over time
 */

import React, { useState } from 'react'

export default function SecurityDriftTimeline({ deltaData }) {
  if (!deltaData || deltaData.status === 'baseline') {
    return (
      <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
        <p className="text-sm text-slate-400">
          📊 Baseline scan recorded. Future scans will show security trends.
        </p>
      </div>
    )
  }

  const { drift, trend } = deltaData
  const { risk_score_change, component_changes, new_risks, improvements } = drift

  const improved = risk_score_change.direction === 'improved'
  const getDirectionIcon = () => improved ? '📈' : '📉'

  return (
    <div className="space-y-4">
      {/* Header with direction */}
      <div className="flex items-center justify-between p-4 rounded-lg bg-gradient-to-r from-slate-800/50 to-slate-900/50 border border-slate-700">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{getDirectionIcon()}</span>
          <div>
            <p className="font-semibold text-slate-200">Security Trend</p>
            <p className="text-sm text-slate-400">{drift.summary}</p>
          </div>
        </div>

        {/* Score change badge */}
        <div
          className={`text-right px-3 py-2 rounded-lg ${
            improved
              ? 'bg-success-neon/10 text-success-neon border border-success-neon/30'
              : 'bg-critical-red/10 text-critical-red border border-critical-red/30'
          }`}
        >
          <p className="text-xl font-black">{risk_score_change.delta > 0 ? '+' : ''}{risk_score_change.delta.toFixed(1)}</p>
          <p className="text-xs opacity-70">points</p>
        </div>
      </div>

      {/* Timeline */}
      <div className="space-y-3">
        {/* Risk Score Change */}
        <div className="p-3 rounded-lg bg-slate-800/30 border border-slate-700">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-slate-300">Risk Score</span>
            <span className="text-xs text-slate-400">
              {risk_score_change.previous} → {risk_score_change.latest}
            </span>
          </div>
          <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-defend-cyan to-defend-blue transition-all duration-300"
              style={{
                width: `${(risk_score_change.latest / 100) * 100}%`,
              }}
            />
          </div>
        </div>

        {/* Component Changes */}
        <div className="grid grid-cols-3 gap-2">
          {/* SSL Status */}
          <div className="p-3 rounded-lg bg-slate-800/30 border border-slate-700">
            <p className="text-xs text-slate-400 mb-1">🔐 SSL</p>
            <p className="text-sm font-semibold text-slate-300">
              {component_changes.ssl === 'no change' ? '✓' : component_changes.ssl === 'fixed' ? '✅' : '❌'}
            </p>
            <p className="text-xs text-slate-400 capitalize">{component_changes.ssl}</p>
          </div>

          {/* Headers Change */}
          <div className="p-3 rounded-lg bg-slate-800/30 border border-slate-700">
            <p className="text-xs text-slate-400 mb-1">📋 Headers</p>
            <p className="text-sm font-semibold text-slate-300">
              {component_changes.missing_headers.delta === 0 ? '→' : component_changes.missing_headers.delta > 0 ? '✅' : '❌'}
            </p>
            <p className="text-xs text-slate-400">
              {component_changes.missing_headers.previous} → {component_changes.missing_headers.latest}
            </p>
          </div>

          {/* Ports Change */}
          <div className="p-3 rounded-lg bg-slate-800/30 border border-slate-700">
            <p className="text-xs text-slate-400 mb-1">🚪 Ports</p>
            <p className="text-sm font-semibold text-slate-300">
              {component_changes.open_ports.delta === 0 ? '→' : component_changes.open_ports.delta > 0 ? '✅' : '❌'}
            </p>
            <p className="text-xs text-slate-400">
              {component_changes.open_ports.previous} → {component_changes.open_ports.latest}
            </p>
          </div>
        </div>

        {/* Improvements */}
        {improvements.length > 0 && (
          <div className="p-3 rounded-lg bg-success-neon/10 border border-success-neon/30">
            <p className="text-xs font-semibold text-success-neon mb-2">✅ Improvements</p>
            <ul className="space-y-1">
              {improvements.map((imp, i) => (
                <li key={i} className="text-xs text-slate-300">
                  • {imp}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* New Risks */}
        {new_risks.length > 0 && (
          <div className="p-3 rounded-lg bg-critical-red/10 border border-critical-red/30">
            <p className="text-xs font-semibold text-critical-red mb-2">⚠️ New Risks</p>
            <ul className="space-y-1">
              {new_risks.map((risk, i) => (
                <li key={i} className="text-xs text-slate-300">
                  • {risk}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Timeline metadata */}
      <div className="text-xs text-slate-400 text-center pt-2">
        {drift.scans_recorded} scans recorded • Last scan: {new Date(drift.latest_timestamp).toLocaleString()}
      </div>
    </div>
  )
}
