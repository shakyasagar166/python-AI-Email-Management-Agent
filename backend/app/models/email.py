"""
Email Entity Model
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Email:
    id: Optional[int] = None
    message_id: Optional[str] = None
    thread_id: Optional[str] = None
    user_id: int = 1
    sender_name: str = ""
    sender_email: str = ""
    recipient_email: str = ""
    subject: str = ""
    body_text: str = ""
    body_html: Optional[str] = None
    snippet: Optional[str] = None
    category_id: Optional[int] = None
    priority: str = "Medium"
    sentiment: str = "Neutral"
    is_read: bool = False
    is_starred: bool = False
    is_archived: bool = False
    is_spam: bool = False
    received_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            message_id=data.get("message_id"),
            thread_id=data.get("thread_id"),
            user_id=int(data.get("user_id", 1)),
            sender_name=data.get("sender_name", ""),
            sender_email=data.get("sender_email", ""),
            recipient_email=data.get("recipient_email", ""),
            subject=data.get("subject", ""),
            body_text=data.get("body_text", ""),
            body_html=data.get("body_html"),
            snippet=data.get("snippet"),
            category_id=int(data["category_id"]) if data.get("category_id") is not None else None,
            priority=data.get("priority", "Medium"),
            sentiment=data.get("sentiment", "Neutral"),
            is_read=bool(data.get("is_read", 0)),
            is_starred=bool(data.get("is_starred", 0)),
            is_archived=bool(data.get("is_archived", 0)),
            is_spam=bool(data.get("is_spam", 0)),
            received_at=str(data.get("received_at")) if data.get("received_at") else None,
            created_at=str(data.get("created_at")) if data.get("created_at") else None,
            updated_at=str(data.get("updated_at")) if data.get("updated_at") else None,
        )
