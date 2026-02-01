/**
 * Open Ports Card Component
 * Displays list of open ports and services
 */

import React from 'react'

export default function OpenPortsCard({ ports }) {
  if (!ports) return null

  const { open_ports, ports_open_count, hostname, error } = ports

  const getDangerLevel = (port) => {
    const dangerousPorts = {
      21: 'danger',
      22: 'warning',
      23: 'danger',
      445: 'danger',
      3306: 'danger',
      5432: 'danger',
      27017: 'danger',
    }
    return dangerousPorts[port] || 'info'
  }

  const colorMap = {
    danger: { bg: 'bg-red-50', border: 'border-red-300', badge: 'bg-red-500' },
    warning: { bg: 'bg-yellow-50', border: 'border-yellow-300', badge: 'bg-yellow-500' },
    info: { bg: 'bg-blue-50', border: 'border-blue-300', badge: 'bg-blue-500' },
  }

  return (
    <div className="rounded-lg shadow-md p-6 bg-white">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-dark">Open Ports</h3>
          <p className="text-xs text-gray-500 mt-1">Scan range: 1-1024</p>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold" style={{
            color: ports_open_count === 0 ? '#10b981' : ports_open_count <= 2 ? '#f59e0b' : '#ef4444'
          }}>
            {ports_open_count}
          </p>
          <p className="text-xs text-gray-500">Port{ports_open_count !== 1 ? 's' : ''} Open</p>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded">
          <p className="text-xs text-error font-semibold">⚠️ {error}</p>
        </div>
      )}

      {ports_open_count === 0 ? (
        <div className="bg-green-50 border border-green-200 rounded p-4 text-center">
          <p className="text-sm text-success font-semibold">✓ No open ports detected</p>
          <p className="text-xs text-gray-600 mt-1">Good security posture</p>
        </div>
      ) : (
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {open_ports.map((portInfo, idx) => {
            const danger = getDangerLevel(portInfo.port)
            const colors = colorMap[danger]

            return (
              <div key={idx} className={`rounded p-3 border ${colors.bg} ${colors.border}`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3 flex-1">
                    <div className={`w-3 h-3 rounded-full ${colors.badge}`}></div>
                    <div>
                      <p className="text-sm font-mono font-semibold text-dark">
                        Port {portInfo.port}
                      </p>
                      <p className="text-xs text-gray-600">{portInfo.service}</p>
                    </div>
                  </div>
                  <div className="text-xs">
                    {danger === 'danger' && <span className="text-error font-bold">⚠️ HIGH RISK</span>}
                    {danger === 'warning' && <span className="text-warning font-bold">⚠️ CAUTION</span>}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {hostname && (
        <div className="mt-4 pt-4 border-t text-xs text-gray-500">
          <p>Scanned: <span className="font-mono">{hostname}</span></p>
        </div>
      )}
    </div>
  )
}
