"""
Email Draft Entity Model
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class EmailDraft:
    id: Optional[int] = None
    email_id: int = 0
    user_id: int = 1
    reply_subject: str = ""
    reply_body: str = ""
    tone: str = "Professional"
    intent: str = "Acknowledge and Resolve"
    status: str = "Draft"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            email_id=int(data.get("email_id", 0)),
            user_id=int(data.get("user_id", 1)),
            reply_subject=data.get("reply_subject", ""),
            reply_body=data.get("reply_body", ""),
            tone=data.get("tone", "Professional"),
            intent=data.get("intent", "Acknowledge and Resolve"),
            status=data.get("status", "Draft"),
            created_at=str(data.get("created_at")) if data.get("created_at") else None,
            updated_at=str(data.get("updated_at")) if data.get("updated_at") else None,
        )
