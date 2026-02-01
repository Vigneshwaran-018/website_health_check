/**
 * Main App Component
 * Root component orchestrating the entire dashboard
 */

import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import URLInput from './components/URLInput'
import LoadingSpinner from './components/LoadingSpinner'
import ErrorDisplay from './components/ErrorDisplay'
import RiskScoreCard from './components/RiskScoreCard'
import SSLStatusCard from './components/SSLStatusCard'
import SecurityHeadersCard from './components/SecurityHeadersCard'
import OpenPortsCard from './components/OpenPortsCard'
import DeductionsTable from './components/DeductionsTable'
import apiService from './services/api'
import { formatTimestamp } from './config'

function App() {
  const [scanResults, setScanResults] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [lastScannedUrl, setLastScannedUrl] = useState(null)

  // Check if backend is available on mount
  useEffect(() => {
    const checkBackend = async () => {
      const result = await apiService.checkHealth()
      if (!result.success) {
        console.warn('Backend may not be available:', result.error)
      }
    }
    checkBackend()
  }, [])

  const handleScan = async (url) => {
    setIsLoading(true)
    setError(null)
    setScanResults(null)

    try {
      const result = await apiService.scanWebsite(url)

      if (result.success) {
        setScanResults(result.data)
        setLastScannedUrl(url)
      } else {
        setError(result.error || 'Failed to scan website. Please check the URL and try again.')
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.')
      console.error('Scan error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDismissError = () => {
    setError(null)
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Header />

      <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* URL Input Section */}
        <URLInput onScan={handleScan} isLoading={isLoading} />

        {/* Loading State */}
        {isLoading && <LoadingSpinner />}

        {/* Error State */}
        {error && !isLoading && (
          <ErrorDisplay error={error} onDismiss={handleDismissError} />
        )}

        {/* Results Section */}
        {scanResults && !isLoading && (
          <div className="fade-in">
            {/* Scan Summary Header */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-2xl font-bold text-dark">Scan Results</h2>
                  <p className="text-sm text-gray-500 mt-1">
                    Website: <span className="font-mono font-semibold text-gray-700">{scanResults.url}</span>
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500">Scanned on:</p>
                  <p className="text-xs text-gray-600 font-mono">
                    {formatTimestamp(scanResults.scan_timestamp)}
                  </p>
                </div>
              </div>

              {/* Quick Summary */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t">
                <div>
                  <p className="text-xs text-gray-500 uppercase">Overall Risk</p>
                  <p className="text-lg font-bold text-dark mt-1">
                    {scanResults.summary.overall_risk}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase">Risk Score</p>
                  <p className="text-lg font-bold text-primary-600 mt-1">
                    {scanResults.summary.risk_score}/100
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase">SSL Status</p>
                  <p className="text-lg font-bold mt-1">
                    {scanResults.summary.ssl_valid ? '✅ Valid' : '❌ Invalid'}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase">Missing Headers</p>
                  <p className="text-lg font-bold text-error mt-1">
                    {scanResults.summary.missing_headers_count}
                  </p>
                </div>
              </div>
            </div>

            {/* Main Results Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
              {/* Risk Score - Larger on left */}
              <div className="lg:col-span-1">
                <RiskScoreCard riskScore={scanResults.risk_score} />
              </div>

              {/* SSL Status */}
              <div className="lg:col-span-1">
                <SSLStatusCard ssl={scanResults.ssl} />
              </div>

              {/* Open Ports */}
              <div className="lg:col-span-1">
                <OpenPortsCard ports={scanResults.ports} />
              </div>
            </div>

            {/* Security Headers - Full Width */}
            <div className="mb-8">
              <SecurityHeadersCard headers={scanResults.headers} />
            </div>

            {/* Deductions Table - Full Width */}
            {scanResults.risk_score?.deductions?.length > 0 && (
              <div className="mb-8">
                <DeductionsTable deductions={scanResults.risk_score.deductions} />
              </div>
            )}

            {/* Recommendations */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-dark mb-4">
                📋 Security Recommendations
              </h3>
              <div className="space-y-3 text-sm text-gray-700">
                {!scanResults.summary.ssl_valid && (
                  <div className="flex items-start space-x-3">
                    <span className="text-lg">🔐</span>
                    <div>
                      <p className="font-medium">Fix SSL Certificate</p>
                      <p className="text-xs text-gray-600 mt-1">
                        Obtain a valid SSL certificate from a trusted Certificate Authority (e.g., Let's Encrypt)
                      </p>
                    </div>
                  </div>
                )}

                {scanResults.summary.missing_headers_count > 0 && (
                  <div className="flex items-start space-x-3">
                    <span className="text-lg">🛡️</span>
                    <div>
                      <p className="font-medium">Add Missing Security Headers</p>
                      <p className="text-xs text-gray-600 mt-1">
                        Configure your web server to send the missing security headers
                      </p>
                    </div>
                  </div>
                )}

                {scanResults.summary.open_ports_count > 0 && (
                  <div className="flex items-start space-x-3">
                    <span className="text-lg">🚪</span>
                    <div>
                      <p className="font-medium">Review Open Ports</p>
                      <p className="text-xs text-gray-600 mt-1">
                        Close unnecessary ports and ensure only required services are exposed
                      </p>
                    </div>
                  </div>
                )}

                {scanResults.summary.risk_score >= 80 && (
                  <div className="flex items-start space-x-3">
                    <span className="text-lg">✅</span>
                    <div>
                      <p className="font-medium">Good Job!</p>
                      <p className="text-xs text-gray-600 mt-1">
                        Your website has a strong security posture. Continue monitoring regularly.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!scanResults && !isLoading && !error && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Ready to Scan</h2>
            <p className="text-gray-600">
              Enter a website URL above to begin a comprehensive security audit
            </p>
          </div>
        )}
      </main>

      <Footer />
    </div>
  )
}

export default App
