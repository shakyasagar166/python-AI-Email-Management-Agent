-- AI Email Management Agent (MailMind)
-- Production Relational Schema

-- Table: Users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(255),
    role VARCHAR(20) NOT NULL DEFAULT 'User',
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Email Categories
CREATE TABLE IF NOT EXISTS email_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    color VARCHAR(20) NOT NULL DEFAULT '#3b82f6',
    description TEXT,
    icon VARCHAR(30) DEFAULT 'mail',
    is_system BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Emails
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id VARCHAR(100) UNIQUE,
    thread_id VARCHAR(100),
    user_id INTEGER NOT NULL,
    sender_name VARCHAR(100) NOT NULL,
    sender_email VARCHAR(120) NOT NULL,
    recipient_email VARCHAR(120) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body_text TEXT NOT NULL,
    body_html TEXT,
    snippet VARCHAR(255),
    category_id INTEGER,
    priority VARCHAR(20) NOT NULL DEFAULT 'Medium', -- Urgent, High, Medium, Low
    sentiment VARCHAR(20) NOT NULL DEFAULT 'Neutral', -- Positive, Neutral, Negative
    is_read BOOLEAN NOT NULL DEFAULT 0,
    is_starred BOOLEAN NOT NULL DEFAULT 0,
    is_archived BOOLEAN NOT NULL DEFAULT 0,
    is_spam BOOLEAN NOT NULL DEFAULT 0,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES email_categories(id) ON DELETE SET NULL
);

-- Table: Email Summaries (AI Extracted)
CREATE TABLE IF NOT EXISTS email_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id INTEGER NOT NULL UNIQUE,
    one_sentence_summary TEXT NOT NULL,
    key_points_json TEXT NOT NULL DEFAULT '[]',
    action_items_json TEXT NOT NULL DEFAULT '[]',
    sentiment_score REAL DEFAULT 0.0,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email_id) REFERENCES emails(id) ON DELETE CASCADE
);

-- Table: Email Drafts (AI Generated or User Authored)
CREATE TABLE IF NOT EXISTS email_drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    reply_subject VARCHAR(255) NOT NULL,
    reply_body TEXT NOT NULL,
    tone VARCHAR(30) NOT NULL DEFAULT 'Professional', -- Professional, Friendly, Direct, Empathetic, Formal
    intent VARCHAR(50) NOT NULL DEFAULT 'Acknowledge and Resolve',
    status VARCHAR(20) NOT NULL DEFAULT 'Draft', -- Draft, Approved, Sent
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email_id) REFERENCES emails(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table: Automation Rules (Agentic triggers & automated actions)
CREATE TABLE IF NOT EXISTS automation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    condition_field VARCHAR(30) NOT NULL, -- sender, subject, category, priority, keyword
    condition_operator VARCHAR(20) NOT NULL, -- contains, equals, starts_with, regex
    condition_value TEXT NOT NULL,
    action_type VARCHAR(30) NOT NULL, -- auto_reply, auto_archive, assign_category, mark_urgent, forward
    action_payload_json TEXT DEFAULT '{}',
    is_enabled BOOLEAN NOT NULL DEFAULT 1,
    execution_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_emails_user ON emails(user_id);
CREATE INDEX IF NOT EXISTS idx_emails_category ON emails(category_id);
CREATE INDEX IF NOT EXISTS idx_emails_priority ON emails(priority);
CREATE INDEX IF NOT EXISTS idx_emails_is_read ON emails(is_read);
CREATE INDEX IF NOT EXISTS idx_emails_received ON emails(received_at);
CREATE INDEX IF NOT EXISTS idx_rules_user ON automation_rules(user_id, is_enabled);
