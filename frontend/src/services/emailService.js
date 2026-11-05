/**
 * Email & AI Services Layer
 */
import { request } from './api'

export const emailService = {
  // Emails
  getEmails: (params = {}) => {
    const query = new URLSearchParams()
    if (params.category_id) query.append('category_id', params.category_id)
    if (params.priority) query.append('priority', params.priority)
    if (params.is_read !== undefined && params.is_read !== '') query.append('is_read', params.is_read)
    if (params.is_starred !== undefined && params.is_starred !== '') query.append('is_starred', params.is_starred)
    if (params.is_archived !== undefined) query.append('is_archived', params.is_archived)
    if (params.search) query.append('search', params.search)
    return request(`/api/emails?${query.toString()}`)
  },

  getEmailById: (id) => request(`/api/emails/${id}`),

  getCategories: () => request('/api/emails/categories'),

  getDashboardStats: () => request('/api/emails/stats/dashboard'),

  setReadStatus: (id, isRead) => request(`/api/emails/${id}/read?is_read=${isRead}`, { method: 'PATCH' }),

  setStarStatus: (id, isStarred) => request(`/api/emails/${id}/star?is_starred=${isStarred}`, { method: 'PATCH' }),

  setArchiveStatus: (id, isArchived) => request(`/api/emails/${id}/archive?is_archived=${isArchived}`, { method: 'PATCH' }),

  deleteEmail: (id) => request(`/api/emails/${id}`, { method: 'DELETE' }),

  sendInboundEmail: (data) => request('/api/emails/inbound', {
    method: 'POST',
    body: JSON.stringify(data)
  }),

  // AI Intelligence
  getAIConfig: () => request('/api/ai/config'),

  analyzeEmail: (id) => request(`/api/ai/analyze-email/${id}`, { method: 'POST' }),

  generateReply: (id, payload) => request(`/api/ai/generate-reply/${id}`, {
    method: 'POST',
    body: JSON.stringify(payload)
  }),

  // Summaries
  getEmailSummary: (id) => request(`/api/summaries/email/${id}`),

  refreshSummary: (id) => request(`/api/summaries/generate/${id}`, { method: 'POST' }),

  // Drafts
  getDrafts: () => request('/api/drafts'),

  saveDraft: (data) => request('/api/drafts', {
    method: 'POST',
    body: JSON.stringify(data)
  }),

  updateDraft: (id, data) => request(`/api/drafts/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),

  deleteDraft: (id) => request(`/api/drafts/${id}`, { method: 'DELETE' }),

  // Automations
  getAutomationRules: () => request('/api/automations'),

  createAutomationRule: (data) => request('/api/automations', {
    method: 'POST',
    body: JSON.stringify(data)
  }),

  toggleAutomationRule: (id) => request(`/api/automations/${id}/toggle`, { method: 'PATCH' }),

  deleteAutomationRule: (id) => request(`/api/automations/${id}`, { method: 'DELETE' })
}
