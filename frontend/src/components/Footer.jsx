/**
 * Footer Component
 */

import React from 'react'

export default function Footer() {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h4 className="font-semibold text-dark mb-2">About</h4>
            <p className="text-sm text-gray-600">
              Security-focused web application for comprehensive website health checks
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-dark mb-2">Important</h4>
            <p className="text-sm text-gray-600">
              ⚠️ Only scan websites you own or have explicit permission to scan. Unauthorized scanning may be illegal.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-dark mb-2">Version</h4>
            <p className="text-sm text-gray-600">
              Health Check Dashboard v1.0.0
            </p>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-200 text-center text-sm text-gray-500">
          <p>&copy; 2024 Health Check Dashboard. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
