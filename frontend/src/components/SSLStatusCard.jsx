/**
 * SSL Status Card Component
 * Displays SSL/TLS certificate information
 */

import React from 'react'

export default function SSLStatusCard({ ssl }) {
  if (!ssl) return null

  const { is_valid, issued_to, issued_by, expires_in_days, protocol_version, cipher, warning, error } = ssl

  const getStatusColor = () => {
    if (error) return 'red'
    if (!is_valid) return 'red'
    if (expires_in_days < 30) return 'yellow'
    return 'green'
  }

  const colorClass = {
    green: 'text-success',
    yellow: 'text-warning',
    red: 'text-error',
  }[getStatusColor()]

  const bgClass = {
    green: 'bg-green-50 border-green-200',
    yellow: 'bg-yellow-50 border-yellow-200',
    red: 'bg-red-50 border-red-200',
  }[getStatusColor()]

  return (
    <div className={`rounded-lg shadow-md p-6 border ${bgClass}`}>
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-lg font-semibold text-dark">SSL/TLS Certificate</h3>
        <div className={`text-2xl ${colorClass}`}>
          {error ? '❌' : is_valid ? '✅' : '⚠️'}
        </div>
      </div>

      <div className="space-y-3">
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wider">Status</p>
          <p className={`text-sm font-semibold ${colorClass}`}>
            {error ? 'Certificate Error' : is_valid ? 'Valid' : 'Invalid'}
          </p>
        </div>

        {issued_to && issued_to !== 'Unknown' && (
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider">Issued To</p>
            <p className="text-sm text-gray-800 font-mono">{issued_to}</p>
          </div>
        )}

        {issued_by && issued_by !== 'Unknown' && (
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider">Issued By</p>
            <p className="text-sm text-gray-800">{issued_by}</p>
          </div>
        )}

        {expires_in_days !== undefined && expires_in_days !== -1 && (
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider">Expires In</p>
            <p className="text-sm text-gray-800">
              {expires_in_days} day{expires_in_days !== 1 ? 's' : ''}
            </p>
          </div>
        )}

        {protocol_version && (
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider">Protocol</p>
            <p className="text-sm text-gray-800 font-mono">{protocol_version}</p>
          </div>
        )}

        {cipher && (
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider">Cipher Suite</p>
            <p className="text-sm text-gray-800 font-mono break-words">{cipher}</p>
          </div>
        )}

        {warning && (
          <div className="mt-4 p-3 bg-warning bg-opacity-10 border border-warning rounded">
            <p className="text-xs text-warning font-semibold">⚠️ {warning}</p>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-error bg-opacity-10 border border-error rounded">
            <p className="text-xs text-error font-semibold">❌ {error}</p>
          </div>
        )}
      </div>
    </div>
  )
}
