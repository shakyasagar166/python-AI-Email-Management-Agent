"""
Pydantic Schemas for Emails, Summaries & AI Drafts
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class EmailCreateRequest(BaseModel):
    sender_name: str
    sender_email: str
    recipient_email: str
    subject: str
    body_text: str
    body_html: Optional[str] = None
    category_id: Optional[int] = None
    priority: Optional[str] = "Medium"


class EmailSummaryResponse(BaseModel):
    id: Optional[int] = None
    email_id: int
    one_sentence_summary: str
    key_points: List[str]
    action_items: List[str]
    sentiment_score: float
    generated_at: Optional[str] = None


class EmailResponse(BaseModel):
    id: int
    message_id: Optional[str] = None
    thread_id: Optional[str] = None
    user_id: int
    sender_name: str
    sender_email: str
    recipient_email: str
    subject: str
    body_text: str
    body_html: Optional[str] = None
    snippet: Optional[str] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    category_color: Optional[str] = None
    priority: str
    sentiment: str
    is_read: bool
    is_starred: bool
    is_archived: bool
    is_spam: bool
    received_at: str
    summary: Optional[EmailSummaryResponse] = None


class DraftCreateRequest(BaseModel):
    email_id: int
    reply_subject: str
    reply_body: str
    tone: Optional[str] = "Professional"
    intent: Optional[str] = "Acknowledge and Resolve"
    status: Optional[str] = "Draft"


class DraftResponse(BaseModel):
    id: int
    email_id: int
    user_id: int
    reply_subject: str
    reply_body: str
    tone: str
    intent: str
    status: str
    created_at: Optional[str] = None


class AIReplyRequest(BaseModel):
    tone: Optional[str] = "Professional"
    custom_instructions: Optional[str] = None
    intent: Optional[str] = "Acknowledge and Resolve"


class AIAnalysisResponse(BaseModel):
    email_id: int
    category_id: int
    category_name: str
    priority: str
    intent: str
    sentiment: str
    one_sentence_summary: str
    key_points: List[str]
    action_items: List[str]
    suggested_reply: str
