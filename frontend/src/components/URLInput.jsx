/**
 * URL Input Component
 * Handles user input for website scanning
 */

import React, { useState } from 'react'

export default function URLInput({ onScan, isLoading }) {
  const [url, setUrl] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')

    if (!url.trim()) {
      setError('Please enter a website URL')
      return
    }

    onScan(url.trim())
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-xl font-semibold text-dark mb-4">Scan a Website</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
            Website URL
          </label>
          <div className="flex space-x-2">
            <input
              id="url"
              type="text"
              value={url}
              onChange={(e) => {
                setUrl(e.target.value)
                setError('')
              }}
              placeholder="e.g., example.com or https://example.com"
              disabled={isLoading}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
            />
            <button
              type="submit"
              disabled={isLoading}
              className={`px-6 py-2 rounded-lg font-medium transition-colors whitespace-nowrap ${
                isLoading
                  ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
                  : 'bg-primary-600 text-white hover:bg-primary-700'
              }`}
            >
              {isLoading ? (
                <span className="flex items-center space-x-2">
                  <span className="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full spin"></span>
                  <span>Scanning...</span>
                </span>
              ) : (
                'Scan Now'
              )}
            </button>
          </div>
          {error && <p className="text-error text-sm mt-2">{error}</p>}
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded p-3">
          <p className="text-xs text-blue-800">
            <strong>⚠️ Note:</strong> Only scan websites you own or have explicit permission to scan. Unauthorized scanning may be illegal.
          </p>
        </div>
      </form>
    </div>
  )
}
