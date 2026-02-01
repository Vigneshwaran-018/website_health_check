/**
 * Security Headers Card Component
 * Displays status of HTTP security headers
 */

import React, { useState } from 'react'

export default function SecurityHeadersCard({ headers }) {
  const [expandedHeader, setExpandedHeader] = useState(null)

  if (!headers) return null

  const { present_headers, missing_headers, missing_count, error } = headers

  const headersScore = present_headers.length > 0
    ? Math.round((present_headers.length / (present_headers.length + missing_count)) * 100)
    : 0

  return (
    <div className="rounded-lg shadow-md p-6 bg-white">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-dark">Security Headers</h3>
          <p className="text-xs text-gray-500 mt-1">
            {present_headers.length + missing_count} total headers checked
          </p>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-primary-600">{headersScore}%</p>
          <p className="text-xs text-gray-500">Coverage</p>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded">
          <p className="text-xs text-error font-semibold">⚠️ {error}</p>
        </div>
      )}

      {/* Present Headers */}
      {present_headers.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-success mb-3 flex items-center">
            <span className="w-2 h-2 bg-success rounded-full mr-2"></span>
            Present ({present_headers.length})
          </h4>
          <div className="space-y-2">
            {present_headers.map((header, idx) => (
              <div
                key={idx}
                className="bg-green-50 border border-green-200 rounded p-3 cursor-pointer hover:bg-green-100 transition"
                onClick={() => setExpandedHeader(expandedHeader === idx ? null : idx)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-mono text-dark">{header.name}</p>
                    <p className="text-xs text-gray-600">{header.description}</p>
                  </div>
                  <span className="text-success text-lg">✓</span>
                </div>
                {expandedHeader === idx && (
                  <div className="mt-2 pt-2 border-t border-green-300">
                    <p className="text-xs text-gray-700 font-mono break-words bg-white p-2 rounded">
                      {header.value}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Missing Headers */}
      {missing_headers.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-error mb-3 flex items-center">
            <span className="w-2 h-2 bg-error rounded-full mr-2"></span>
            Missing ({missing_headers.length})
          </h4>
          <div className="space-y-2">
            {missing_headers.map((header, idx) => (
              <div key={idx} className="bg-red-50 border border-red-200 rounded p-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-mono text-dark">{header.name}</p>
                    <p className="text-xs text-gray-600">{header.description}</p>
                  </div>
                  <span className="text-error text-lg">✗</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
