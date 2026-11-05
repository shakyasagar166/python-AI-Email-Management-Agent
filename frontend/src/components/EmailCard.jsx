import React from 'react'
import { Star, Sparkles, Archive, Trash2, Mail, MailOpen } from 'lucide-react'

export default function EmailCard({
  email,
  onSelect,
  onToggleStar,
  onToggleRead,
  onToggleArchive,
  onDelete
}) {
  const getPriorityBadgeClass = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'urgent': return 'badge-urgent'
      case 'high': return 'badge-high'
      case 'medium': return 'badge-medium'
      default: return 'badge-low'
    }
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return ''
    try {
      const d = new Date(dateStr)
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    } catch {
      return dateStr
    }
  }

  return (
    <div
      className={`email-item ${!email.is_read ? 'unread' : ''}`}
      onClick={() => onSelect && onSelect(email)}
    >
      <div
        style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={() => onToggleStar && onToggleStar(email.id, !email.is_starred)}
          title={email.is_starred ? 'Unstar' : 'Star'}
          style={{ color: email.is_starred ? '#f59e0b' : '#cbd5e1' }}
        >
          <Star size={18} fill={email.is_starred ? '#f59e0b' : 'none'} />
        </button>

        <button
          onClick={() => onToggleRead && onToggleRead(email.id, !email.is_read)}
          title={email.is_read ? 'Mark as Unread' : 'Mark as Read'}
          style={{ color: '#94a3b8' }}
        >
          {email.is_read ? <MailOpen size={16} /> : <Mail size={16} color="#6366f1" />}
        </button>
      </div>

      <div className="email-sender">
        <div style={{ fontWeight: !email.is_read ? 700 : 500, color: 'var(--text-main)' }}>
          {email.sender_name || email.sender_email}
        </div>
      </div>

      <div className="email-content">
        <div className="email-subject-line">
          <span className={`badge ${getPriorityBadgeClass(email.priority)}`}>
            {email.priority}
          </span>

          {email.category_name && (
            <span
              className="badge"
              style={{
                backgroundColor: `${email.category_color}15`,
                color: email.category_color || '#475569',
                borderColor: `${email.category_color}30`
              }}
            >
              {email.category_name}
            </span>
          )}

          <span className="email-subject">{email.subject}</span>
        </div>

        <div className="email-snippet">
          {email.summary?.one_sentence_summary ? (
            <span style={{ color: '#4f46e5', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <Sparkles size={12} />
              {email.summary.one_sentence_summary}
            </span>
          ) : (
            email.snippet || email.body_text?.substring(0, 100) + '...'
          )}
        </div>
      </div>

      <div className="email-meta" onClick={(e) => e.stopPropagation()}>
        <span>{formatDate(email.received_at)}</span>

        <button
          onClick={() => onToggleArchive && onToggleArchive(email.id, !email.is_archived)}
          title={email.is_archived ? 'Unarchive' : 'Archive'}
          className="btn-secondary"
          style={{ padding: '0.3rem 0.5rem', borderRadius: '4px' }}
        >
          <Archive size={14} />
        </button>

        {onDelete && (
          <button
            onClick={() => onDelete(email.id)}
            title="Delete"
            className="btn-danger"
            style={{ padding: '0.3rem 0.5rem', borderRadius: '4px' }}
          >
            <Trash2 size={14} />
          </button>
        )}
      </div>
    </div>
  )
}
