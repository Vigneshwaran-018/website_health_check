/**
 * Header Component
 * Navigation and branding
 */

import React from 'react'

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-primary-700 to-primary-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-white rounded-lg">
              <span className="text-primary-700 font-bold text-lg">🛡️</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold">Health Check Dashboard</h1>
              <p className="text-sm text-primary-100">Website Security Audit Tool</p>
            </div>
          </div>
          <div className="text-right text-xs text-primary-100">
            <p>Comprehensive Security Scanning</p>
          </div>
        </div>
      </div>
    </header>
  )
}
