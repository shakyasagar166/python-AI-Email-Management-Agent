"""
Email Summary Entity Model
"""
import json
from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class EmailSummary:
    id: Optional[int] = None
    email_id: int = 0
    one_sentence_summary: str = ""
    key_points: List[str] = None
    action_items: List[str] = None
    sentiment_score: float = 0.0
    generated_at: Optional[str] = None

    def __post_init__(self):
        if self.key_points is None:
            self.key_points = []
        if self.action_items is None:
            self.action_items = []

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        kp = data.get("key_points") or data.get("key_points_json") or []
        if isinstance(kp, str):
            try:
                kp = json.loads(kp)
            except Exception:
                kp = []

        act = data.get("action_items") or data.get("action_items_json") or []
        if isinstance(act, str):
            try:
                act = json.loads(act)
            except Exception:
                act = []

        return cls(
            id=data.get("id"),
            email_id=int(data.get("email_id", 0)),
            one_sentence_summary=data.get("one_sentence_summary", ""),
            key_points=kp,
            action_items=act,
            sentiment_score=float(data.get("sentiment_score", 0.0)),
            generated_at=str(data.get("generated_at")) if data.get("generated_at") else None,
        )
