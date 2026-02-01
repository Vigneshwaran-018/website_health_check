/**
 * Environment and configuration utilities
 */

/**
 * Get configuration based on environment
 */
export const getConfig = () => {
  const isDevelopment = import.meta.env.DEV
  
  return {
    apiUrl: import.meta.env.VITE_API_URL || (isDevelopment ? 'http://localhost:8000' : '/api'),
    environment: isDevelopment ? 'development' : 'production',
    isDevelopment,
  }
}

/**
 * Logger utility for debugging
 */
export const logger = {
  log: (message, data = null) => {
    console.log(`[Health Check] ${message}`, data || '')
  },
  error: (message, error = null) => {
    console.error(`[Health Check Error] ${message}`, error || '')
  },
  warn: (message, data = null) => {
    console.warn(`[Health Check Warning] ${message}`, data || '')
  },
}

/**
 * Utility to format timestamp
 */
export const formatTimestamp = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleString()
}

/**
 * Utility to format numbers
 */
export const formatNumber = (num) => {
  return new Intl.NumberFormat().format(num)
}
