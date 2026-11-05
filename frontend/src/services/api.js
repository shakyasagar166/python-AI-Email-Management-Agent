/**
 * MailMind AI - Base Fetch Client
 */
const BASE_URL = '' // Uses Vite proxy in development

export async function request(endpoint, options = {}) {
  const token = localStorage.getItem('token')
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {})
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers
  })

  if (!response.ok) {
    let errorDetail = 'Network request failed'
    try {
      const errJson = await response.json()
      errorDetail = errJson.message || errJson.detail || errorDetail
    } catch (e) {
      // Fallback
    }
    throw new Error(errorDetail)
  }

  return response.json()
}
