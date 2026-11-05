import React, { useEffect, useState } from 'react'
import {
  Sliders,
  Plus,
  Play,
  Trash2,
  CheckCircle2,
  XCircle,
  X,
  RefreshCw,
  Zap,
  ArrowRight
} from 'lucide-react'
import { emailService } from '../services/emailService'

export default function AutomationRules() {
  const [rules, setRules] = useState([])
  const [loading, setLoading] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [newRule, setNewRule] = useState({
    name: '',
    description: '',
    condition_field: 'subject',
    condition_operator: 'contains',
    condition_value: '',
    action_type: 'auto_archive',
    action_payload: {}
  })

  useEffect(() => {
    loadRules()
  }, [])

  const loadRules = async () => {
    setLoading(true)
    try {
      const data = await emailService.getAutomationRules()
      setRules(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleToggle = async (ruleId) => {
    try {
      await emailService.toggleAutomationRule(ruleId)
      setRules((prev) =>
        prev.map((r) => (r.id === ruleId ? { ...r, is_enabled: !r.is_enabled } : r))
      )
    } catch (err) {
      alert(`Toggle failed: ${err.message}`)
    }
  }

  const handleDelete = async (ruleId) => {
    if (window.confirm('Delete this automation rule?')) {
      await emailService.deleteAutomationRule(ruleId)
      setRules((prev) => prev.filter((r) => r.id !== ruleId))
    }
  }

  const handleCreateRule = async (e) => {
    e.preventDefault()
    if (!newRule.name || !newRule.condition_value) {
      alert('Rule name and match value are required.')
      return
    }

    try {
      await emailService.createAutomationRule(newRule)
      setIsModalOpen(false)
      setNewRule({
        name: '',
        description: '',
        condition_field: 'subject',
        condition_operator: 'contains',
        condition_value: '',
        action_type: 'auto_archive',
        action_payload: {}
      })
      loadRules()
    } catch (err) {
      alert(`Creation failed: ${err.message}`)
    }
  }

  const formatAction = (actionType) => {
    switch (actionType) {
      case 'mark_urgent': return 'Escalate to Urgent Priority'
      case 'auto_archive': return 'Automatically Archive'
      case 'assign_category': return 'Assign Custom Category'
      case 'auto_reply': return 'Auto-Dispatch Acknowledgment'
      default: return actionType
    }
  }

  return (
    <div className="page-wrapper">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Inbound Automation Rules</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Event-driven triggers that execute automatically when new inbounds arrive
          </p>
        </div>

        <button onClick={() => setIsModalOpen(true)} className="btn btn-primary">
          <Plus size={16} />
          <span>New Automation Rule</span>
        </button>
      </div>

      <div className="card">
        {loading ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>
            <RefreshCw size={24} className="spin" style={{ margin: '0 auto 0.75rem' }} />
            <div>Loading rules engine...</div>
          </div>
        ) : rules.length === 0 ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>
            <Zap size={36} style={{ margin: '0 auto 0.75rem', opacity: 0.5 }} />
            <div style={{ fontWeight: 600, fontSize: '1rem', color: '#475569' }}>No automation rules active</div>
            <p style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>
              Create a rule to automate archiving, priority escalation, or instant replies.
            </p>
          </div>
        ) : (
          <div>
            {rules.map((rule) => (
              <div
                key={rule.id}
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
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.35rem' }}>
                    <span style={{ fontWeight: 700, fontSize: '1rem', color: '#0f172a' }}>
                      {rule.name}
                    </span>
                    <span
                      className="badge"
                      style={{
                        backgroundColor: rule.is_enabled ? '#ecfdf5' : '#f1f5f9',
                        color: rule.is_enabled ? '#059669' : '#94a3b8',
                        border: `1px solid ${rule.is_enabled ? '#a7f3d0' : '#e2e8f0'}`
                      }}
                    >
                      {rule.is_enabled ? 'Active' : 'Paused'}
                    </span>
                    <span style={{ fontSize: '0.775rem', color: '#64748b' }}>
                      Executed: <strong>{rule.execution_count} times</strong>
                    </span>
                  </div>

                  <p style={{ fontSize: '0.825rem', color: '#64748b', marginBottom: '0.5rem' }}>
                    {rule.description || 'Custom autonomous workflow rule'}
                  </p>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.825rem' }}>
                    <span style={{ background: '#f8fafc', padding: '0.25rem 0.5rem', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                      IF <strong>{rule.condition_field}</strong> {rule.condition_operator} <code>"{rule.condition_value}"</code>
                    </span>
                    <ArrowRight size={14} color="#94a3b8" />
                    <span style={{ background: '#eef2ff', color: '#4338ca', padding: '0.25rem 0.5rem', borderRadius: '4px', fontWeight: 600 }}>
                      THEN {formatAction(rule.action_type)}
                    </span>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  <button
                    onClick={() => handleToggle(rule.id)}
                    className="btn btn-secondary"
                    style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem' }}
                  >
                    {rule.is_enabled ? 'Pause' : 'Activate'}
                  </button>

                  <button
                    onClick={() => handleDelete(rule.id)}
                    className="btn btn-danger"
                    style={{ padding: '0.45rem 0.65rem' }}
                    title="Delete Rule"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* New Rule Modal */}
      {isModalOpen && (
        <div className="modal-overlay" onClick={() => setIsModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3 style={{ fontSize: '1.2rem', fontWeight: 800 }}>Create Automation Workflow Rule</h3>
              <button onClick={() => setIsModalOpen(false)} style={{ color: '#94a3b8' }}>
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleCreateRule}>
              <div className="form-group">
                <label className="form-label">Rule Name</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g., Auto-escalate security incident alerts"
                  value={newRule.name}
                  onChange={(e) => setNewRule({ ...newRule, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Description (Optional)</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="Briefly describe what this workflow accomplishes"
                  value={newRule.description}
                  onChange={(e) => setNewRule({ ...newRule, description: e.target.value })}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div className="form-group">
                  <label className="form-label">Evaluate Field</label>
                  <select
                    className="form-select"
                    value={newRule.condition_field}
                    onChange={(e) => setNewRule({ ...newRule, condition_field: e.target.value })}
                  >
                    <option value="subject">Subject</option>
                    <option value="sender_email">Sender Email</option>
                    <option value="sender_name">Sender Name</option>
                    <option value="priority">Priority</option>
                    <option value="body">Body Text</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Operator</label>
                  <select
                    className="form-select"
                    value={newRule.condition_operator}
                    onChange={(e) => setNewRule({ ...newRule, condition_operator: e.target.value })}
                  >
                    <option value="contains">Contains (Case Insensitive)</option>
                    <option value="equals">Equals Exact Match</option>
                    <option value="starts_with">Starts With</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Value to Match</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g., [SECURITY] or pagerduty.com"
                  value={newRule.condition_value}
                  onChange={(e) => setNewRule({ ...newRule, condition_value: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Target Automated Action</label>
                <select
                  className="form-select"
                  value={newRule.action_type}
                  onChange={(e) => setNewRule({ ...newRule, action_type: e.target.value })}
                >
                  <option value="auto_archive">Auto-Archive (Move out of active inbox)</option>
                  <option value="mark_urgent">Escalate to Urgent Priority</option>
                  <option value="auto_reply">Send Automated Confirmation Reply</option>
                </select>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
                <button type="button" onClick={() => setIsModalOpen(false)} className="btn btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Save & Enable Rule
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
