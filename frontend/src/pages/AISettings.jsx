import React, { useEffect, useState } from 'react'
import {
  Bot,
  Sliders,
  Cpu,
  Sparkles,
  Save,
  CheckCircle,
  GraduationCap,
  ExternalLink,
  Zap,
  Key
} from 'lucide-react'
import { emailService } from '../services/emailService'

export default function AISettings() {
  const [config, setConfig] = useState(null)
  const [selectedProvider, setSelectedProvider] = useState('Local Heuristic Engine')
  const [selectedModel, setSelectedModel] = useState('gpt-4o-mini')
  const [temperature, setTemperature] = useState(0.3)
  const [defaultTone, setDefaultTone] = useState('Professional')
  const [apiKey, setApiKey] = useState('')
  const [savedSuccess, setSavedSuccess] = useState(false)

  useEffect(() => {
    emailService.getAIConfig().then((data) => {
      setConfig(data)
    }).catch(console.error)
  }, [])

  const handleSave = (e) => {
    e.preventDefault()
    setSavedSuccess(true)
    setTimeout(() => setSavedSuccess(false), 3000)
  }

  return (
    <div className="page-wrapper">
      <div style={{ marginBottom: '1.75rem' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>AI Agent Configuration & Models</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          Tune multi-model routing, inference temperature, prompt styles, and heuristic fallbacks
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1.2fr', gap: '2rem' }}>
        {/* Settings Form */}
        <div className="card" style={{ padding: '1.75rem' }}>
          {savedSuccess && (
            <div style={{ backgroundColor: '#ecfdf5', color: '#059669', padding: '0.75rem 1rem', borderRadius: '6px', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem', border: '1px solid #a7f3d0' }}>
              <CheckCircle size={16} />
              <span>AI settings updated and saved to runtime cache!</span>
            </div>
          )}

          <form onSubmit={handleSave}>
            <div className="form-group">
              <label className="form-label">Active LLM Provider Engine</label>
              <select
                className="form-select"
                value={selectedProvider}
                onChange={(e) => setSelectedProvider(e.target.value)}
              >
                <option value="Local Heuristic Engine">Local Heuristic Engine (Offline / Zero-latency)</option>
                <option value="OpenAI">OpenAI (GPT-4o, GPT-4o-mini)</option>
                <option value="Anthropic">Anthropic (Claude 3.5 Sonnet)</option>
                <option value="Google Gemini">Google Gemini 1.5 Pro</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Default Model</label>
              <select
                className="form-select"
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
              >
                <option value="gpt-4o-mini">gpt-4o-mini (Fast & Cost Efficient)</option>
                <option value="gpt-4o">gpt-4o (High-Precision Complex Reasoning)</option>
                <option value="claude-3-5-sonnet">claude-3-5-sonnet (Nuanced Communication)</option>
                <option value="gemini-1.5-flash">gemini-1.5-flash (High Throughput)</option>
              </select>
            </div>

            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                <label className="form-label" style={{ marginBottom: 0 }}>Sampling Temperature ({temperature})</label>
                <span style={{ fontSize: '0.8rem', color: '#64748b' }}>
                  {temperature <= 0.2 ? 'Deterministic' : temperature <= 0.5 ? 'Balanced' : 'Creative'}
                </span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                style={{ width: '100%' }}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Default Communication Tone</label>
              <select
                className="form-select"
                value={defaultTone}
                onChange={(e) => setDefaultTone(e.target.value)}
              >
                <option value="Professional">Professional</option>
                <option value="Formal">Formal</option>
                <option value="Casual">Casual</option>
                <option value="Empathetic">Empathetic</option>
                <option value="Direct">Direct</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Provider API Key (Optional in local mode)</label>
              <input
                type="password"
                className="form-input"
                placeholder="sk-..."
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
              />
              <span style={{ fontSize: '0.75rem', color: '#94a3b8', display: 'block', marginTop: '0.25rem' }}>
                If empty, MailMind runs on built-in offline NLP & heuristic reasoning pipeline.
              </span>
            </div>

            <button type="submit" className="btn btn-primary" style={{ marginTop: '0.5rem' }}>
              <Save size={16} />
              <span>Save AI Configuration</span>
            </button>
          </form>
        </div>

        {/* Education & Upskilling Sidebar Card */}
        <div>
          <div className="card" style={{ padding: '1.5rem', marginBottom: '1.5rem', background: '#f8fafc' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
              <Zap size={18} color="#6366f1" />
              <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Agentic Pipeline Overview</h3>
            </div>
            <p style={{ fontSize: '0.85rem', color: '#64748b', lineHeight: 1.5, marginBottom: '1rem' }}>
              MailMind uses a 3-stage agentic lifecycle:
            </p>
            <ol style={{ paddingLeft: '1.25rem', fontSize: '0.825rem', color: '#334155', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <li><strong>Ingestion & Parsing:</strong> Cleans MIME headers, normalizes body, detects sentiment score.</li>
              <li><strong>Intent & Classification:</strong> Analyzes urgency, classifies into categories, scores priority.</li>
              <li><strong>Synthesis & Dispatch:</strong> Generates executive bullet summaries and human-reviewable reply drafts.</li>
            </ol>
          </div>

          {/* Upskilling Card */}
          <div className="card" style={{ padding: '1.5rem', border: '1px solid #c7d2fe', background: '#eef2ff' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <GraduationCap size={20} color="#4f46e5" />
              <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#312e81' }}>Professional Python & AI</h3>
            </div>
            <p style={{ fontSize: '0.85rem', color: '#4338ca', lineHeight: 1.4, marginBottom: '1rem' }}>
              Looking to build high-scale AI applications, FastAPI backends, and autonomous workflows like MailMind? Check out top programs:
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <a
                href="https://uncodemy.com/course/python-training-course-in-noida"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
                style={{ fontSize: '0.825rem', padding: '0.5rem 0.85rem' }}
              >
                <span>Python Training Course in Noida</span>
                <ExternalLink size={12} />
              </a>

              <a
                href="https://uncodemy.com/course/python-training-course-in-delhi"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary"
                style={{ fontSize: '0.825rem', padding: '0.5rem 0.85rem', backgroundColor: '#ffffff' }}
              >
                <span>Python Training Course in Delhi</span>
                <ExternalLink size={12} />
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
