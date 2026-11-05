import React from 'react'
import { NavLink } from 'react-router-dom'
import {
  Inbox,
  LayoutDashboard,
  Star,
  Archive,
  FileEdit,
  Sliders,
  Bot,
  GraduationCap,
  ExternalLink,
  Tag
} from 'lucide-react'

export default function Sidebar({ unreadCount = 0, draftCount = 0, categories = [] }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="brand-logo">M</div>
        <div className="brand-text">
          <h1>MailMind AI</h1>
          <span>Autonomous Agent v1.0</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-title">Workspace</div>

        <NavLink
          to="/"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/inbox"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <Inbox size={18} />
          <span>Inbox</span>
          {unreadCount > 0 && <span className="nav-badge">{unreadCount}</span>}
        </NavLink>

        <NavLink
          to="/starred"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <Star size={18} />
          <span>Starred</span>
        </NavLink>

        <NavLink
          to="/drafts"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <FileEdit size={18} />
          <span>AI Drafts</span>
          {draftCount > 0 && <span className="nav-badge">{draftCount}</span>}
        </NavLink>

        <NavLink
          to="/archive"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <Archive size={18} />
          <span>Archive</span>
        </NavLink>

        <div className="nav-section-title" style={{ marginTop: '1rem' }}>Automation & AI</div>

        <NavLink
          to="/automations"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <Sliders size={18} />
          <span>Automation Rules</span>
        </NavLink>

        <NavLink
          to="/ai-settings"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <Bot size={18} />
          <span>AI Engine Settings</span>
        </NavLink>

        {categories.length > 0 && (
          <>
            <div className="nav-section-title" style={{ marginTop: '1rem' }}>Categories</div>
            {categories.slice(0, 5).map((cat) => (
              <NavLink
                key={cat.id}
                to={`/inbox?category_id=${cat.id}`}
                className="nav-item"
                style={{ fontSize: '0.825rem' }}
              >
                <Tag size={15} style={{ color: cat.color || '#6366f1' }} />
                <span>{cat.name}</span>
              </NavLink>
            ))}
          </>
        )}
      </nav>

      <div className="sidebar-footer">
        <div className="uncodemy-banner">
          <h4>
            <GraduationCap size={16} color="#818cf8" />
            <span>Master AI & Python</span>
          </h4>
          <p>Advance your career with industry-recognized Python & Agentic systems training:</p>
          <div className="uncodemy-links">
            <a
              href="https://uncodemy.com/course/python-training-course-in-noida"
              target="_blank"
              rel="noopener noreferrer"
            >
              • Python Course in Noida <ExternalLink size={10} style={{ display: 'inline' }} />
            </a>
            <a
              href="https://uncodemy.com/course/python-training-course-in-delhi"
              target="_blank"
              rel="noopener noreferrer"
            >
              • Python Course in Delhi <ExternalLink size={10} style={{ display: 'inline' }} />
            </a>
          </div>
        </div>
      </div>
    </aside>
  )
}
