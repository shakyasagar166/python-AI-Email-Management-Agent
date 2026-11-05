import React, { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import {
  Inbox as InboxIcon,
  Filter,
  Plus,
  RefreshCw,
  Send,
  AlertCircle
} from 'lucide-react'
import { emailService } from '../services/emailService'
import EmailCard from '../components/EmailCard'
import AIReplyEditor from '../components/AIReplyEditor'
import EmailDetails from './EmailDetails'

export default function Inbox({ searchTerm }) {
  const [searchParams, setSearchParams] = useSearchParams()
  const [emails, setEmails] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedEmail, setSelectedEmail] = useState(null)
  const [replyingEmail, setReplyingEmail] = useState(null)
  const [filterPriority, setFilterPriority] = useState(searchParams.get('priority') || '')
  const [filterCategory, setFilterCategory] = useState(searchParams.get('category_id') || '')
  const [activeTab, setActiveTab] = useState('all') // all, unread, starred, archive

  useEffect(() => {
    loadCategories()
  }, [])

  useEffect(() => {
    loadEmails()
  }, [filterPriority, filterCategory, activeTab, searchTerm])

  const loadCategories = async () => {
    try {
      const cats = await emailService.getCategories()
      setCategories(cats)
    } catch (e) {
      console.error(e)
    }
  }

  const loadEmails = async () => {
    setLoading(true)
    try {
      const params = {
        priority: filterPriority || undefined,
        category_id: filterCategory || undefined,
        search: searchTerm || undefined
      }

      if (activeTab === 'unread') params.is_read = 0
      if (activeTab === 'starred') params.is_starred = 1
      if (activeTab === 'archive') params.is_archived = 1
      else params.is_archived = 0

      const data = await emailService.getEmails(params)
      setEmails(data)
    } catch (err) {
      console.error('Failed to load emails:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleToggleStar = async (id, isStarred) => {
    await emailService.setStarStatus(id, isStarred)
    setEmails((prev) => prev.map((e) => (e.id === id ? { ...e, is_starred: isStarred ? 1 : 0 } : e)))
  }

  const handleToggleRead = async (id, isRead) => {
    await emailService.setReadStatus(id, isRead)
    setEmails((prev) => prev.map((e) => (e.id === id ? { ...e, is_read: isRead ? 1 : 0 } : e)))
  }

  const handleToggleArchive = async (id, isArchived) => {
    await emailService.setArchiveStatus(id, isArchived)
    loadEmails()
  }

  const handleDelete = async (id) => {
    if (window.confirm('Delete this email permanently?')) {
      await emailService.deleteEmail(id)
      setEmails((prev) => prev.filter((e) => e.id !== id))
    }
  }

  return (
    <div className="page-wrapper">
      {/* Header & Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Inbound Message Stream</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Triaged, prioritized, and summarized by MailMind Autonomous Agent
          </p>
        </div>

        <button onClick={loadEmails} className="btn btn-secondary" title="Refresh messages">
          <RefreshCw size={15} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Tabs & Filters Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', gap: '1rem', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', gap: '0.5rem', background: '#f1f5f9', padding: '0.25rem', borderRadius: '8px' }}>
          {['all', 'unread', 'starred', 'archive'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: '0.45rem 1rem',
                borderRadius: '6px',
                fontSize: '0.85rem',
                fontWeight: 600,
                textTransform: 'capitalize',
                backgroundColor: activeTab === tab ? '#ffffff' : 'transparent',
                color: activeTab === tab ? '#0f172a' : '#64748b',
                boxShadow: activeTab === tab ? '0 1px 3px rgba(0,0,0,0.1)' : 'none'
              }}
            >
              {tab}
            </button>
          ))}
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          {/* Priority filter */}
          <select
            className="form-select"
            style={{ width: 'auto', padding: '0.45rem 0.75rem', fontSize: '0.85rem' }}
            value={filterPriority}
            onChange={(e) => setFilterPriority(e.target.value)}
          >
            <option value="">All Priorities</option>
            <option value="Urgent">Urgent</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>

          {/* Category filter */}
          <select
            className="form-select"
            style={{ width: 'auto', padding: '0.45rem 0.75rem', fontSize: '0.85rem' }}
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
          >
            <option value="">All Categories</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Email List Card */}
      <div className="card">
        {loading ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>
            <RefreshCw size={24} className="spin" style={{ margin: '0 auto 0.75rem' }} />
            <div>Syncing and evaluating inbox streams...</div>
          </div>
        ) : emails.length === 0 ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>
            <InboxIcon size={36} style={{ margin: '0 auto 0.75rem', opacity: 0.5 }} />
            <div style={{ fontWeight: 600, fontSize: '1rem', color: '#475569' }}>No emails match this filter</div>
            <p style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>Change your criteria or refresh the inbox.</p>
          </div>
        ) : (
          emails.map((email) => (
            <EmailCard
              key={email.id}
              email={email}
              onSelect={(selected) => setSelectedEmail(selected)}
              onToggleStar={handleToggleStar}
              onToggleRead={handleToggleRead}
              onToggleArchive={handleToggleArchive}
              onDelete={handleDelete}
            />
          ))
        )}
      </div>

      {/* Full Email Viewer Modal */}
      {selectedEmail && (
        <EmailDetails
          email={selectedEmail}
          onClose={() => setSelectedEmail(null)}
          onOpenReply={(emailToReply) => {
            setSelectedEmail(null)
            setReplyingEmail(emailToReply)
          }}
          onRefresh={loadEmails}
        />
      )}

      {/* AI Reply Modal */}
      {replyingEmail && (
        <AIReplyEditor
          email={replyingEmail}
          onClose={() => setReplyingEmail(null)}
          onDraftSaved={loadEmails}
          onReplySent={loadEmails}
        />
      )}
    </div>
  )
}
