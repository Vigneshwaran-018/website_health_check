/**
 * Error Display Component
 */

import React from 'react'

export default function ErrorDisplay({ error, onDismiss }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <span className="text-2xl">❌</span>
          <div>
            <h4 className="font-semibold text-error">Scan Failed</h4>
            <p className="text-sm text-gray-700 mt-1">{error}</p>
          </div>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  )
}
