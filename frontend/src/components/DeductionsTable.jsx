/**
 * Deductions Table Component
 * Shows scoring breakdown and deductions
 */

import React from 'react'

export default function DeductionsTable({ deductions }) {
  if (!deductions || deductions.length === 0) return null

  return (
    <div className="rounded-lg shadow-md p-6 bg-white">
      <h3 className="text-lg font-semibold text-dark mb-4">Security Deductions</h3>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b-2 border-gray-200">
              <th className="text-left py-3 px-4 font-semibold text-dark">Category</th>
              <th className="text-left py-3 px-4 font-semibold text-dark">Issue</th>
              <th className="text-right py-3 px-4 font-semibold text-dark">Deduction</th>
            </tr>
          </thead>
          <tbody>
            {deductions.map((deduction, idx) => (
              <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium text-gray-700">{deduction.category}</td>
                <td className="py-3 px-4 text-gray-600">{deduction.issue}</td>
                <td className="text-right py-3 px-4 font-semibold text-error">-{deduction.deduction}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
