/**
 * Risk Score Card Component
 * Displays overall risk score with gauge visualization
 */

import React from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'

export default function RiskScoreCard({ riskScore }) {
  if (!riskScore) return null

  const { score, risk_level, risk_color } = riskScore
  
  const colorMap = {
    green: '#10b981',
    yellow: '#f59e0b',
    orange: '#f97316',
    red: '#ef4444',
  }

  const scoreColor = colorMap[risk_color] || '#6b7280'

  // Create gauge data
  const gaugeData = [
    { name: 'Score', value: score },
    { name: 'Remaining', value: 100 - score },
  ]

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-dark mb-4">Security Risk Score</h3>
      
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={gaugeData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                fill={scoreColor}
                dataKey="value"
                startAngle={180}
                endAngle={0}
              >
                <Cell fill={scoreColor} />
                <Cell fill="#e5e7eb" />
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="flex-1 flex flex-col items-center justify-center">
          <div className="text-center">
            <p className="text-5xl font-bold" style={{ color: scoreColor }}>
              {score}
            </p>
            <p className="text-gray-500 text-sm mt-1">/ 100</p>
            
            <div className={`mt-4 px-4 py-2 rounded-full inline-block font-semibold text-white`}
                 style={{ backgroundColor: scoreColor }}>
              {risk_level} Risk
            </div>

            <p className="text-xs text-gray-500 mt-3">
              {score >= 80 && 'Excellent security posture'}
              {score >= 60 && score < 80 && 'Good security, minor improvements recommended'}
              {score >= 40 && score < 60 && 'Multiple security concerns should be addressed'}
              {score < 40 && 'Critical security issues require immediate attention'}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
