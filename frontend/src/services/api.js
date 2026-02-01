/**
 * API Service Configuration and Client
 * Handles all communication with the backend
 */

import axios from 'axios'

// Configuration - can be overridden by environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Create axios instance with default config
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 second timeout for scans
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * API Service Object
 * Provides methods for all backend endpoints
 */
const apiService = {
  /**
   * Health check endpoint
   * Verifies backend is running
   */
  checkHealth: async () => {
    try {
      const response = await apiClient.get('/health')
      return {
        success: true,
        data: response.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error.message,
      }
    }
  },

  /**
   * Full scan endpoint
   * Performs comprehensive security audit
   *
   * @param {string} url - Website URL to scan
   * @returns {Promise} Scan results
   */
  scanWebsite: async (url) => {
    try {
      if (!url || typeof url !== 'string') {
        throw new Error('Invalid URL provided')
      }

      const response = await apiClient.get('/scan', {
        params: {
          url: url.trim(),
        },
      })

      return {
        success: true,
        data: response.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
        status: error.response?.status,
      }
    }
  },

  /**
   * Quick scan endpoint
   * Returns only critical metrics
   *
   * @param {string} url - Website URL to scan
   * @returns {Promise} Quick scan results
   */
  quickScan: async (url) => {
    try {
      if (!url || typeof url !== 'string') {
        throw new Error('Invalid URL provided')
      }

      const response = await apiClient.get('/scan/quick', {
        params: {
          url: url.trim(),
        },
      })

      return {
        success: true,
        data: response.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
        status: error.response?.status,
      }
    }
  },

  /**
   * Set API base URL (useful for switching between environments)
   *
   * @param {string} url - New API base URL
   */
  setApiUrl: (url) => {
    apiClient.defaults.baseURL = url
  },

  /**
   * Get current API base URL
   * @returns {string} Current API base URL
   */
  getApiUrl: () => {
    return apiClient.defaults.baseURL
  },
}

export default apiService
export { API_BASE_URL }
