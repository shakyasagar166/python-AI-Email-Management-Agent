"""
Prompt Engineering Templates for Email Intelligence
"""

EMAIL_CLASSIFICATION_PROMPT = """
You are an expert executive email triage AI. Categorize the incoming email into one of these exact categories:
- Action Required
- Client Inquiry
- Billing & Invoices
- Support & Tickets
- Primary & Internal
- Newsletters & Updates
- Education & Training

Email Subject: {subject}
Sender: {sender}
Body:
{body}

Respond strictly in valid JSON format:
{{
  "category": "Exact Category Name",
  "confidence": 0.95,
  "reasoning": "One-line justification"
}}
"""

EMAIL_SUMMARIZATION_PROMPT = """
Analyze the following email and extract an executive summary, key decision points, and concrete action items.

Email Subject: {subject}
Sender: {sender}
Body:
{body}

Respond strictly in valid JSON format:
{{
  "one_sentence_summary": "Crisp 15-25 word executive takeaway.",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "action_items": ["Action 1", "Action 2"],
  "sentiment_score": 0.75
}}
"""

REPLY_GENERATION_PROMPT = """
Draft an executive, contextual email reply to the following correspondence.

Original Email Subject: {subject}
Original Sender: {sender}
Original Content:
{body}

Target Tone: {tone}
Intent / Goal: {intent}
Custom Directives: {custom_instructions}

Respond strictly in valid JSON format:
{{
  "reply_subject": "Re: {subject}",
  "reply_body": "Full body text of the drafted response with greeting and signoff.",
  "tone": "{tone}",
  "confidence": 0.92
}}
"""
