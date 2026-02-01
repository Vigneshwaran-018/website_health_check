/**
 * Loading Spinner Component
 */

import React from 'react'

export default function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="text-center">
        <div className="inline-block">
          <div className="w-12 h-12 border-4 border-gray-200 border-t-primary-600 rounded-full spin"></div>
        </div>
        <p className="text-gray-600 mt-4">Scanning website security...</p>
        <p className="text-xs text-gray-500 mt-2">This may take 10-30 seconds</p>
      </div>
    </div>
  )
}
