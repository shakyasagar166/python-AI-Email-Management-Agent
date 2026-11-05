import React, { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Inbox from './pages/Inbox'
import Drafts from './pages/Drafts'
import AISettings from './pages/AISettings'
import AutomationRules from './pages/AutomationRules'
import { emailService } from './services/emailService'

function AppLayout() {
  const [searchTerm, setSearchTerm] = useState('')
  const [categories, setCategories] = useState([])
  const [stats, setStats] = useState(null)

  useEffect(() => {
    loadGlobalData()
  }, [])

  const loadGlobalData = async () => {
    try {
      const [cats, dashboardStats] = await Promise.all([
        emailService.getCategories(),
        emailService.getDashboardStats()
      ])
      setCategories(cats || [])
      setStats(dashboardStats)
    } catch (e) {
      console.error('Failed to load global data:', e)
    }
  }

  const unreadCount = stats?.metrics?.unread_count || 0
  const draftCount = stats?.draft_count || 0

  return (
    <div className="app-container">
      <Sidebar
        unreadCount={unreadCount}
        draftCount={draftCount}
        categories={categories}
      />

      <div className="main-content">
        <Navbar searchTerm={searchTerm} onSearchChange={setSearchTerm} />

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/inbox" element={<Inbox searchTerm={searchTerm} />} />
          <Route path="/starred" element={<Inbox searchTerm={searchTerm} />} />
          <Route path="/archive" element={<Inbox searchTerm={searchTerm} />} />
          <Route path="/drafts" element={<Drafts />} />
          <Route path="/automations" element={<AutomationRules />} />
          <Route path="/ai-settings" element={<AISettings />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppLayout />
      </BrowserRouter>
    </AuthProvider>
  )
}
