import React, { useEffect, useState } from 'react'
import { FileEdit, Trash2, Send, RefreshCw, Sparkles, MessageSquare } from 'lucide-react'
import { emailService } from '../services/emailService'
import AIReplyEditor from '../components/AIReplyEditor'

export default function Drafts() {
  const [drafts, setDrafts] = useState([])
  const [loading, setLoading] = useState(true)
  const [editingDraft, setEditingDraft] = useState(null)

  useEffect(() => {
    loadDrafts()
  }, [])

  const loadDrafts = async () => {
    setLoading(true)
    try {
      const data = await emailService.getDrafts()
      setDrafts(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteDraft = async (id) => {
    if (window.confirm('Discard this draft permanently?')) {
      await emailService.deleteDraft(id)
      setDrafts((prev) => prev.filter((d) => d.id !== id))
    }
  }

  return (
    <div className="page-wrapper">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>AI Generated & Stored Drafts</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Contextual reply candidates waiting for human-in-the-loop approval or dispatch
          </p>
        </div>

        <button onClick={loadDrafts} className="btn btn-secondary">
          <RefreshCw size={15} />
          <span>Refresh</span>
        </button>
      </div>

      <div className="card">
        {loading ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>
            <RefreshCw size={24} className="spin" style={{ margin: '0 auto 0.75rem' }} />
            <div>Loading saved drafts...</div>
          </div>
        ) : drafts.length === 0 ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>
            <FileEdit size={36} style={{ margin: '0 auto 0.75rem', opacity: 0.5 }} />
            <div style={{ fontWeight: 600, fontSize: '1rem', color: '#475569' }}>No pending drafts</div>
            <p style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>
              Open any inbox message and click "Generate AI Reply" to build intelligent drafts.
            </p>
          </div>
        ) : (
          <div>
            {drafts.map((draft) => (
              <div
                key={draft.id}
                style={{
                  padding: '1.25rem 1.5rem',
                  borderBottom: '1px solid #f1f5f9',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '1rem'
                }}
              >
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.35rem' }}>
                    <span className="badge badge-category">Tone: {draft.tone}</span>
                    <span className="badge" style={{ backgroundColor: '#ecfdf5', color: '#059669', border: '1px solid #a7f3d0' }}>
                      {draft.status || 'Draft'}
                    </span>
                    <span style={{ fontSize: '0.8rem', color: '#64748b' }}>
                      To: <strong>{draft.sender_email || 'Inbound Recipient'}</strong>
                    </span>
                  </div>

                  <h3 style={{ fontSize: '0.975rem', fontWeight: 700, color: '#0f172a', marginBottom: '0.25rem' }}>
                    {draft.reply_subject}
                  </h3>

                  <p style={{ fontSize: '0.85rem', color: '#64748b', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {draft.reply_body}
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  <button
                    onClick={() => setEditingDraft({
                      id: draft.email_id,
                      subject: draft.reply_subject.replace(/^Re:\s*/i, ''),
                      sender_email: draft.sender_email
                    })}
                    className="btn btn-primary"
                    style={{ padding: '0.45rem 0.9rem', fontSize: '0.825rem' }}
                  >
                    <FileEdit size={14} />
                    <span>Review & Edit</span>
                  </button>

                  <button
                    onClick={() => handleDeleteDraft(draft.id)}
                    className="btn btn-danger"
                    style={{ padding: '0.45rem 0.65rem' }}
                    title="Discard Draft"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {editingDraft && (
        <AIReplyEditor
          email={editingDraft}
          onClose={() => setEditingDraft(null)}
          onDraftSaved={loadDrafts}
          onReplySent={loadDrafts}
        />
      )}
    </div>
  )
}
