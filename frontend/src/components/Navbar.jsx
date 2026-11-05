import React from 'react'
import { Search, Sparkles, BookOpen, ExternalLink, Bell } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Navbar({ searchTerm, onSearchChange }) {
  const { user } = useAuth()

  return (
    <header className="navbar">
      <div className="nav-search">
        <Search size={18} color="#94a3b8" />
        <input
          type="text"
          placeholder="Search emails by sender, subject, or AI keywords..."
          value={searchTerm || ''}
          onChange={(e) => onSearchChange && onSearchChange(e.target.value)}
        />
      </div>

      <div className="navbar-right">
        {/* Upskill / Training Link Pills */}
        <a
          href="https://uncodemy.com/course/python-training-course-in-noida"
          target="_blank"
          rel="noopener noreferrer"
          className="training-pill"
          title="Learn Python & AI Engineering at Uncodemy Noida"
        >
          <BookOpen size={14} />
          <span>Python Noida</span>
          <ExternalLink size={12} />
        </a>

        <a
          href="https://uncodemy.com/course/python-training-course-in-delhi"
          target="_blank"
          rel="noopener noreferrer"
          className="training-pill"
          title="Master Agentic AI & Backend Development at Uncodemy Delhi"
        >
          <Sparkles size={14} />
          <span>Python Delhi</span>
          <ExternalLink size={12} />
        </a>

        <div className="user-profile-badge">
          <div className="avatar">
            {user?.full_name ? user.full_name.charAt(0) : 'U'}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{user?.full_name || 'Shivam Shakya'}</span>
            <span style={{ fontSize: '0.725rem', color: '#64748b' }}>{user?.role || 'Admin'}</span>
          </div>
        </div>
      </div>
    </header>
  )
}
