"""
Automation Rule Entity Model
"""
import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class AutomationRule:
    id: Optional[int] = None
    user_id: int = 1
    name: str = ""
    description: Optional[str] = None
    condition_field: str = "sender"
    condition_operator: str = "contains"
    condition_value: str = ""
    action_type: str = "assign_category"
    action_payload: Dict[str, Any] = None
    is_enabled: bool = True
    execution_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.action_payload is None:
            self.action_payload = {}

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        payload = data.get("action_payload") or data.get("action_payload_json") or {}
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {}

        return cls(
            id=data.get("id"),
            user_id=int(data.get("user_id", 1)),
            name=data.get("name", ""),
            description=data.get("description"),
            condition_field=data.get("condition_field", "sender"),
            condition_operator=data.get("condition_operator", "contains"),
            condition_value=data.get("condition_value", ""),
            action_type=data.get("action_type", "assign_category"),
            action_payload=payload,
            is_enabled=bool(data.get("is_enabled", 1)),
            execution_count=int(data.get("execution_count", 0)),
            created_at=str(data.get("created_at")) if data.get("created_at") else None,
            updated_at=str(data.get("updated_at")) if data.get("updated_at") else None,
        )
