import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Inbox,
  AlertTriangle,
  FileEdit,
  Sliders,
  Sparkles,
  ArrowRight,
  GraduationCap,
  ExternalLink,
  ShieldCheck,
  CheckCircle2
} from 'lucide-react'
import { emailService } from '../services/emailService'
import EmailCard from '../components/EmailCard'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [urgentEmails, setUrgentEmails] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const data = await emailService.getDashboardStats()
      setStats(data)

      const emails = await emailService.getEmails({ priority: 'Urgent', is_archived: 0 })
      setUrgentEmails(emails.slice(0, 3))
    } catch (err) {
      console.error('Failed to load dashboard:', err)
    } finally {
      setLoading(false)
    }
  }

  const metrics = stats?.metrics || {}

  return (
    <div className="page-wrapper">
      {/* Hero Welcome */}
      <div style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.02em' }}>
            Autonomous Email Operations
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '0.25rem' }}>
            Real-time multi-agent classification, intent synthesis, and contextual reply automation.
          </p>
        </div>

        <Link to="/inbox" className="btn btn-primary">
          <Inbox size={16} />
          <span>Open Full Inbox</span>
          <ArrowRight size={14} />
        </Link>
      </div>

      {/* Stats KPI Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#e0e7ff', color: '#4f46e5' }}>
            <Inbox size={24} />
          </div>
          <div className="stat-info">
            <h3>{metrics.total_inbox ?? 0}</h3>
            <p>Total Emails Ingested</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#ecfdf5', color: '#059669' }}>
            <CheckCircle2 size={24} />
          </div>
          <div className="stat-info">
            <h3>{metrics.unread_count ?? 0}</h3>
            <p>Unread Inbounds</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#fef2f2', color: '#dc2626' }}>
            <AlertTriangle size={24} />
          </div>
          <div className="stat-info">
            <h3>{metrics.urgent_count ?? 0}</h3>
            <p>Urgent Priority Items</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#f5f3ff', color: '#7c3aed' }}>
            <FileEdit size={24} />
          </div>
          <div className="stat-info">
            <h3>{stats?.draft_count ?? 0}</h3>
            <p>AI Drafts Generated</p>
          </div>
        </div>
      </div>

      {/* Main Grid: Urgent Attention & Category Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1.2fr', gap: '1.75rem', marginBottom: '2.5rem' }}>
        {/* Urgent Action Needed */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <AlertTriangle size={18} color="#ef4444" />
              <h2 className="card-title">Urgent Inbounds Needing Response</h2>
            </div>
            <Link to="/inbox?priority=Urgent" style={{ fontSize: '0.825rem', color: '#6366f1', fontWeight: 600 }}>
              View all
            </Link>
          </div>

          <div>
            {urgentEmails.length === 0 ? (
              <div style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8' }}>
                No urgent priority emails requiring immediate attention.
              </div>
            ) : (
              urgentEmails.map((email) => (
                <EmailCard key={email.id} email={email} />
              ))
            )}
          </div>
        </div>

        {/* Category Distribution */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Category Ingestion Breakdown</h2>
          </div>

          <div style={{ padding: '1.25rem' }}>
            {stats?.category_breakdown?.map((cat, idx) => (
              <div key={idx} style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.35rem' }}>
                  <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: cat.color || '#6366f1' }}></span>
                    {cat.name}
                  </span>
                  <span style={{ color: 'var(--text-muted)' }}>{cat.count} emails</span>
                </div>
                <div style={{ width: '100%', height: '8px', backgroundColor: '#f1f5f9', borderRadius: '4px', overflow: 'hidden' }}>
                  <div
                    style={{
                      height: '100%',
                      width: `${Math.min(100, (cat.count / Math.max(1, metrics.total_inbox || 1)) * 100)}%`,
                      backgroundColor: cat.color || '#6366f1',
                      borderRadius: '4px'
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Featured Training & Upskilling Banner */}
      <div style={{
        background: 'linear-gradient(135deg, #1e1b4b, #312e81)',
        borderRadius: '16px',
        padding: '2rem',
        color: '#ffffff',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: 'var(--shadow-md)'
      }}>
        <div style={{ maxWidth: '650px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(255, 255, 255, 0.1)', padding: '0.3rem 0.75rem', borderRadius: '9999px', fontSize: '0.8rem', marginBottom: '0.75rem', color: '#c7d2fe' }}>
            <GraduationCap size={16} />
            <span>Official Python & AI Engineering Partner</span>
          </div>
          <h2 style={{ fontSize: '1.45rem', fontWeight: 800, marginBottom: '0.5rem' }}>
            Build Agentic Workflows & Master Enterprise Python
          </h2>
          <p style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: 1.5 }}>
            Accelerate your career in software engineering, machine learning, and autonomous agent architecture with specialized hands-on programs:
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <a
            href="https://uncodemy.com/course/python-training-course-in-noida"
            target="_blank"
            rel="noopener noreferrer"
            className="btn"
            style={{ backgroundColor: '#ffffff', color: '#312e81', fontWeight: 700 }}
          >
            <span>Python Training in Noida</span>
            <ExternalLink size={14} />
          </a>

          <a
            href="https://uncodemy.com/course/python-training-course-in-delhi"
            target="_blank"
            rel="noopener noreferrer"
            className="btn"
            style={{ backgroundColor: 'rgba(255, 255, 255, 0.15)', color: '#ffffff', border: '1px solid rgba(255, 255, 255, 0.3)' }}
          >
            <span>Python Training in Delhi</span>
            <ExternalLink size={14} />
          </a>
        </div>
      </div>
    </div>
  )
}
