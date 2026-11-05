import React, { useState } from 'react'
import { Sparkles, Send, Save, X, Bot, RefreshCw } from 'lucide-react'
import { emailService } from '../services/emailService'

export default function AIReplyEditor({
  email,
  onClose,
  onDraftSaved,
  onReplySent
}) {
  const [tone, setTone] = useState('Professional')
  const [intent, setIntent] = useState('Acknowledge and Resolve')
  const [instructions, setInstructions] = useState('')
  const [subject, setSubject] = useState(`Re: ${email?.subject || ''}`)
  const [body, setBody] = useState('')
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)

  const handleGenerateReply = async () => {
    if (!email?.id) return
    setLoading(true)
    try {
      const res = await emailService.generateReply(email.id, {
        tone,
        intent,
        custom_instructions: instructions
      })
      if (res?.draft) {
        setSubject(res.draft.reply_subject || subject)
        setBody(res.draft.reply_body || '')
      }
    } catch (err) {
      alert(`AI generation failed: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveDraft = async () => {
    if (!body.trim()) {
      alert('Draft body cannot be empty.')
      return
    }
    setSaving(true)
    try {
      await emailService.saveDraft({
        email_id: email.id,
        reply_subject: subject,
        reply_body: body,
        tone,
        intent,
        status: 'Draft'
      })
      alert('Draft saved successfully!')
      if (onDraftSaved) onDraftSaved()
    } catch (err) {
      alert(`Save failed: ${err.message}`)
    } finally {
      setSaving(false)
    }
  }

  const handleSend = async () => {
    if (!body.trim()) {
      alert('Cannot send an empty email.')
      return
    }
    setSaving(true)
    try {
      // Save draft as Sent status
      await emailService.saveDraft({
        email_id: email.id,
        reply_subject: subject,
        reply_body: body,
        tone,
        intent,
        status: 'Sent'
      })
      alert(`Reply sent to ${email.sender_email}!`)
      if (onReplySent) onReplySent()
      if (onClose) onClose()
    } catch (err) {
      alert(`Send failed: ${err.message}`)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sparkles size={20} color="#6366f1" />
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>AI Intelligent Reply Generator</h3>
          </div>
          <button onClick={onClose} style={{ color: '#94a3b8' }}>
            <X size={20} />
          </button>
        </div>

        {/* AI Parameters Control Panel */}
        <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', marginBottom: '1.25rem', border: '1px solid #e2e8f0' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '0.75rem' }}>
            <div>
              <label className="form-label">Response Tone</label>
              <select
                className="form-select"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
              >
                <option value="Professional">Professional & Courteous</option>
                <option value="Formal">Formal & Executive</option>
                <option value="Casual">Casual & Friendly</option>
                <option value="Empathetic">Empathetic & Supportive</option>
                <option value="Direct">Concise & Direct</option>
              </select>
            </div>

            <div>
              <label className="form-label">Primary Objective / Intent</label>
              <select
                className="form-select"
                value={intent}
                onChange={(e) => setIntent(e.target.value)}
              >
                <option value="Acknowledge and Resolve">Acknowledge & Resolve</option>
                <option value="Schedule Meeting">Confirm / Schedule Meeting</option>
                <option value="Request Information">Request Additional Info</option>
                <option value="Confirm Agreement">Confirm Terms & Agree</option>
              </select>
            </div>
          </div>

          <div style={{ marginBottom: '0.75rem' }}>
            <label className="form-label">Custom Directives / Key Points to Include (Optional)</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g., Mention we can meet Thursday at 3 PM and attach SLA docs."
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
            />
          </div>

          <button
            onClick={handleGenerateReply}
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%' }}
          >
            {loading ? (
              <>
                <RefreshCw size={16} className="spin" />
                <span>Synthesizing Context & Generating Draft...</span>
              </>
            ) : (
              <>
                <Bot size={16} />
                <span>Generate Reply with AI Agent</span>
              </>
            )}
          </button>
        </div>

        {/* Draft Editor */}
        <div className="form-group">
          <label className="form-label">Subject</label>
          <input
            type="text"
            className="form-input"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Reply Message Body</label>
          <textarea
            className="form-textarea"
            rows={10}
            placeholder="AI draft will appear here, or you can write manually..."
            value={body}
            onChange={(e) => setBody(e.target.value)}
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1rem' }}>
          <button onClick={onClose} className="btn btn-secondary">
            Cancel
          </button>

          <button
            onClick={handleSaveDraft}
            disabled={saving || !body}
            className="btn btn-secondary"
          >
            <Save size={16} />
            <span>Save as Draft</span>
          </button>

          <button
            onClick={handleSend}
            disabled={saving || !body}
            className="btn btn-primary"
          >
            <Send size={16} />
            <span>Send Reply</span>
          </button>
        </div>
      </div>
    </div>
  )
}
