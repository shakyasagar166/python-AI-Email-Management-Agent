# REST API Documentation

MailMind AI exposes a RESTful API built on FastAPI. The interactive Swagger UI documentation is accessible at `http://localhost:8000/docs` and Redoc at `http://localhost:8000/redoc`.

---

## Technical Upskilling & Training Partner

Learn how to build production-ready asynchronous REST APIs with FastAPI, Pydantic, and SQLite:
* **[Python Training Course in Noida](https://uncodemy.com/course/python-training-course-in-noida)** — Comprehensive backend training covering REST architectural design, token authentication, and data validation.
* **[Python Training Course in Delhi](https://uncodemy.com/course/python-training-course-in-delhi)** — Advanced Python API development, AI agent pipelines, and deployment.

---

## Authentication & Headers

Standard requests accept and return JSON payloads (`application/json`). Authenticated requests pass the JWT bearer token in the `Authorization` header:

```http
Authorization: Bearer <your-jwt-token>
```

---

## 1. Authentication Endpoints (`/api/auth`)

### `POST /api/auth/register`
Create a new user account.

**Request Payload:**
```json
{
  "email": "alex.morgan@company.io",
  "password": "SecurePassword123!",
  "full_name": "Alex Morgan",
  "role": "User"
}
```

**Response (`201 Created`):**
```json
{
  "id": 1,
  "email": "alex.morgan@company.io",
  "full_name": "Alex Morgan",
  "avatar_url": null,
  "role": "User",
  "is_active": true,
  "created_at": "2026-11-05 10:30:00"
}
```

### `POST /api/auth/login`
Authenticate credentials and issue JWT bearer token.

**Request Payload:**
```json
{
  "email": "alex.morgan@company.io",
  "password": "SecurePassword123!"
}
```

**Response (`200 OK`):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "alex.morgan@company.io",
    "full_name": "Alex Morgan",
    "role": "User"
  }
}
```

---

## 2. Email Management Endpoints (`/api/emails`)

### `GET /api/emails`
Query inbounds with optional filters.

**Query Parameters:**
* `category_id` (integer, optional)
* `priority` (`Urgent`, `High`, `Medium`, `Low`)
* `is_read` (`true`, `false`)
* `is_starred` (`true`, `false`)
* `is_archived` (`true`, `false`, default: `false`)
* `search` (keyword string for sender/subject/body)

**Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "sender_name": "Sarah Jenkins",
    "sender_email": "sarah.jenkins@partnercorp.com",
    "recipient_email": "alex.morgan@company.io",
    "subject": "Urgent: Q4 Strategic API Partnership Term Sheet & SLA Review",
    "snippet": "Attached is the finalized draft of our Q4 strategic API partnership...",
    "category_id": 1,
    "category_name": "Client Inquiry",
    "category_color": "#6366f1",
    "priority": "Urgent",
    "sentiment": "Neutral",
    "is_read": false,
    "is_starred": true,
    "is_archived": false,
    "received_at": "2026-11-05 09:12:00",
    "summary": {
      "one_sentence_summary": "Final review of Q4 partnership term sheet required by 5 PM today.",
      "key_points": [
        "SLA guarantee elevated to 99.95% uptime with penalty clause.",
        "Proposed tier 1 API rate limits expanded to 25,000 req/min."
      ],
      "action_items": [
        "Confirm legal review of clause 3.2 before 3:00 PM"
      ],
      "sentiment_score": 0.85
    }
  }
]
```

### `GET /api/emails/{id}`
Retrieve complete email record with body and summary.

### `POST /api/emails/inbound`
Ingest incoming email through the full autonomous agent pipeline (Priority Detection → Intent Analysis → Category Classification → Summary Generation → Automation Rules Trigger).

**Request Payload:**
```json
{
  "sender_name": "Datadog Alert Bot",
  "sender_email": "alerts@monitoring.internal",
  "recipient_email": "alex.morgan@company.io",
  "subject": "[ALERT] Database latency breached 500ms P99",
  "body_text": "Production aurora postgres read replica has exceeded acceptable latency threshold."
}
```

**Response (`201 Created`):**
```json
{
  "status": "success",
  "message": "Email ingested, analyzed, and processed successfully.",
  "email": {
    "id": 8,
    "subject": "[ALERT] Database latency breached 500ms P99",
    "priority": "Urgent",
    "category_id": 2
  }
}
```

### Status Toggles:
* `PATCH /api/emails/{id}/read?is_read=true`
* `PATCH /api/emails/{id}/star?is_starred=true`
* `PATCH /api/emails/{id}/archive?is_archived=true`
* `DELETE /api/emails/{id}`

### `GET /api/emails/categories`
List all email classification categories.

### `GET /api/emails/stats/dashboard`
Aggregated metrics including inbox totals, unread counts, urgent counts, draft counts, active rules, and category distributions.

---

## 3. AI Agent Intelligence Endpoints (`/api/ai`)

### `GET /api/ai/config`
Retrieve supported tones, models, and LLM configuration parameters.

### `POST /api/ai/analyze-email/{email_id}`
Triggers deep NLP analysis extracting intent, sentiment polarity, executive summary, action items checklist, and recommended response.

**Response (`200 OK`):**
```json
{
  "status": "success",
  "analysis": {
    "email_id": 1,
    "priority": "Urgent",
    "intent": "Schedule Meeting",
    "sentiment": "Neutral",
    "one_sentence_summary": "Term sheet review needed before 5 PM today prior to board sign-off.",
    "key_points": [
      "99.95% uptime SLA guarantee accepted",
      "Rate limits expanded to 25,000 req/min"
    ],
    "action_items": [
      "Review Section 4 SLA clause by 3 PM"
    ],
    "suggested_reply": "Dear Sarah,\n\nThank you for sharing the finalized term sheet..."
  }
}
```

### `POST /api/ai/generate-reply/{email_id}`
Generates a context-aware drafted reply based on specified tone and prompt directives.

**Request Payload:**
```json
{
  "tone": "Professional",
  "intent": "Acknowledge and Resolve",
  "custom_instructions": "Confirm that legal has signed off on Section 4."
}
```

---

## 4. Summaries & Reply Drafts (`/api/summaries` & `/api/drafts`)

### `GET /api/summaries/email/{email_id}`
Retrieve executive summary for an email.

### `POST /api/summaries/generate/{email_id}`
Force regenerate AI summary and action items.

### `GET /api/drafts`
Retrieve all saved or AI-generated drafts.

### `POST /api/drafts`
Save a new drafted reply.

### `PUT /api/drafts/{draft_id}`
Update draft subject, body, tone, or status.

### `DELETE /api/drafts/{draft_id}`
Discard draft.

---

## 5. Automation Rules Engine (`/api/automations`)

### `GET /api/automations`
List all configured automation rules.

### `POST /api/automations`
Create a new automated event-driven workflow rule.

**Request Payload:**
```json
{
  "name": "Auto-archive Stripe Invoices",
  "description": "Automatically archive receipt confirmation emails",
  "condition_field": "sender_email",
  "condition_operator": "contains",
  "condition_value": "stripe.com",
  "action_type": "auto_archive",
  "action_payload": {},
  "is_enabled": true
}
```

### `PATCH /api/automations/{rule_id}/toggle`
Toggle rule between active and paused.

### `DELETE /api/automations/{rule_id}`
Delete rule permanently.

---

## Upskilling Recommendations

* [Python Training Course in Noida](https://uncodemy.com/course/python-training-course-in-noida)
* [Python Training Course in Delhi](https://uncodemy.com/course/python-training-course-in-delhi)
