import React, { useEffect, useState } from 'react'
import {
  X,
  Sparkles,
  Bot,
  Reply,
  Star,
  Archive,
  CheckCircle,
  Tag,
  AlertCircle,
  Clock,
  User
} from 'lucide-react'
import { emailService } from '../services/emailService'

export default function EmailDetails({ email: initialEmail, onClose, onOpenReply, onRefresh }) {
  const [email, setEmail] = useState(initialEmail)
  const [loadingAnalysis, setLoadingAnalysis] = useState(false)

  useEffect(() => {
    // If not read, automatically mark read
    if (!email.is_read) {
      emailService.setReadStatus(email.id, true).then(() => {
        setEmail((prev) => ({ ...prev, is_read: 1 }))
        if (onRefresh) onRefresh()
      })
    }
  }, [email.id])

  const handleDeepAIAnalyze = async () => {
    setLoadingAnalysis(true)
    try {
      const res = await emailService.analyzeEmail(email.id)
      if (res?.analysis) {
        setEmail((prev) => ({
          ...prev,
          summary: {
            one_sentence_summary: res.analysis.one_sentence_summary,
            key_points: res.analysis.key_points,
            action_items: res.analysis.action_items,
            sentiment_score: prev.summary?.sentiment_score || 0.0
          },
          sentiment: res.analysis.sentiment,
          priority: res.analysis.priority
        }))
        alert('Deep AI analysis refreshed!')
      }
    } catch (err) {
      alert(`AI Analysis failed: ${err.message}`)
    } finally {
      setLoadingAnalysis(false)
    }
  }

  const getPriorityBadgeClass = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'urgent': return 'badge-urgent'
      case 'high': return 'badge-high'
      case 'medium': return 'badge-medium'
      default: return 'badge-low'
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-content"
        style={{ maxWidth: '850px', maxHeight: '88vh' }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span className={`badge ${getPriorityBadgeClass(email.priority)}`}>
              {email.priority}
            </span>
            {email.category_name && (
              <span className="badge badge-category">
                {email.category_name}
              </span>
            )}
            <span style={{ fontSize: '0.8rem', color: '#64748b' }}>
              Sentiment: <strong>{email.sentiment || 'Neutral'}</strong>
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button
              onClick={handleDeepAIAnalyze}
              disabled={loadingAnalysis}
              className="btn btn-secondary"
              style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}
              title="Force Deep AI Re-Analysis"
            >
              <Sparkles size={14} color="#6366f1" />
              <span>{loadingAnalysis ? 'Analyzing...' : 'Deep AI Scan'}</span>
            </button>
            <button onClick={onClose} style={{ color: '#94a3b8' }}>
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Email Subject & Sender Meta */}
        <div style={{ marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800, marginBottom: '0.75rem', color: '#0f172a' }}>
            {email.subject}
          </h2>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #f1f5f9', paddingBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div className="avatar">
                {email.sender_name?.charAt(0) || 'U'}
              </div>
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{email.sender_name}</div>
                <div style={{ color: '#64748b', fontSize: '0.8rem' }}>{email.sender_email} &rarr; {email.recipient_email}</div>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#94a3b8', fontSize: '0.8rem' }}>
              <Clock size={14} />
              <span>{new Date(email.received_at).toLocaleString()}</span>
            </div>
          </div>
        </div>

        {/* AI Executive Summary Card */}
        {email.summary && (
          <div className="ai-summary-box">
            <div className="ai-summary-header">
              <Bot size={18} />
              <span>MailMind Executive AI Synthesis</span>
            </div>

            <p className="ai-summary-text">
              {email.summary.one_sentence_summary}
            </p>

            {/* Key Points */}
            {email.summary.key_points && email.summary.key_points.length > 0 && (
              <div style={{ marginBottom: '0.75rem' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#4338ca', marginBottom: '0.35rem' }}>
                  Key Points:
                </div>
                <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', color: '#1e1b4b' }}>
                  {email.summary.key_points.map((pt, i) => (
                    <li key={i} style={{ marginBottom: '0.2rem' }}>{pt}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Action Items */}
            {email.summary.action_items && email.summary.action_items.length > 0 && (
              <div>
                <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#4338ca', marginBottom: '0.35rem' }}>
                  Action Items & Required Decisions:
                </div>
                <div className="action-items-list">
                  {email.summary.action_items.map((act, i) => (
                    <div key={i} className="action-item">
                      <CheckCircle size={14} color="#6366f1" />
                      <span>{act}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Email Full Body */}
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', color: '#64748b', marginBottom: '0.5rem' }}>
            Original Message Body
          </div>
          <div
            style={{
              padding: '1.25rem',
              backgroundColor: '#f8fafc',
              borderRadius: '8px',
              border: '1px solid #e2e8f0',
              fontSize: '0.925rem',
              lineHeight: 1.6,
              color: '#334155',
              whiteSpace: 'pre-wrap'
            }}
          >
            {email.body_text}
          </div>
        </div>

        {/* Action Controls Footer */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #e2e8f0', paddingTop: '1.25rem' }}>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              onClick={() => emailService.setStarStatus(email.id, !email.is_starred).then(() => setEmail(p => ({ ...p, is_starred: !p.is_starred })))}
              className="btn btn-secondary"
            >
              <Star size={16} fill={email.is_starred ? '#f59e0b' : 'none'} color={email.is_starred ? '#f59e0b' : 'currentColor'} />
              <span>{email.is_starred ? 'Starred' : 'Star'}</span>
            </button>

            <button
              onClick={() => emailService.setArchiveStatus(email.id, !email.is_archived).then(() => { if (onRefresh) onRefresh(); onClose(); })}
              className="btn btn-secondary"
            >
              <Archive size={16} />
              <span>{email.is_archived ? 'Unarchive' : 'Archive'}</span>
            </button>
          </div>

          <button
            onClick={() => onOpenReply && onOpenReply(email)}
            className="btn btn-primary"
            style={{ padding: '0.65rem 1.5rem', fontWeight: 700 }}
          >
            <Sparkles size={16} />
            <span>Generate AI Reply</span>
            <Reply size={16} />
          </button>
        </div>
      </div>
    </div>
  )
}
